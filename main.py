import os
import time
from datetime import datetime

import requests

# Constants
API_KEY = os.getenv("KRAKENFLEX_API_KEY", "EltgJ5G8m44IzwE6UN2Y4B4NjPW77Zk6FJK3lL23")
API_BASE_URL = "https://api.krakenflex.systems/interview-tests-mock-api/v1"
TARGET_SITE = "norwich-pear-tree"
MIN_DATE = "2022-01-01T00:00:00.000Z"
MAX_RETRIES = 5
INITIAL_BACKOFF = 1  # seconds

# Headers for API requests
api_headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}


def perform_request_with_retries(url, method='get', data=None):
    """
    Perform an API request with retries in case of 500 errors.

    Args:
        url (str): The URL for the API endpoint.
        method (str): The HTTP method ('get' or 'post').
        data (dict): The data to send in a POST request.

    Returns:
        dict: The JSON response from the API if successful, None otherwise.
    """
    attempt = 0
    backoff = INITIAL_BACKOFF

    while attempt < MAX_RETRIES:
        try:
            if method == 'get':
                response = requests.get(url, headers=api_headers)
            elif method == 'post':
                response = requests.post(url, headers=api_headers, json=data)
            else:
                raise ValueError("Invalid HTTP method specified.")

            if response.status_code == 500:
                raise requests.exceptions.RequestException(f"Server error: {response.status_code}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request error on attempt {attempt + 1}: {e}")
            if attempt == MAX_RETRIES - 1:
                print(f"Max retries reached. Failed to get a successful response from {url}.")
                return None
            attempt += 1
            time.sleep(backoff)
            backoff *= 2  # Exponential backoff

    return None


def fetch_all_outages():
    """
    Fetches all outage data from the outages endpoint.

    Returns:
        list: A list containing all outages as dictionaries.
    """
    return perform_request_with_retries(f"{API_BASE_URL}/outages")


def fetch_site_details(site_id):
    """
    Retrieves information about a specific site, including device details.

    Args:
        site_id (str): The ID of the site to retrieve details for.

    Returns:
        dict: A dictionary containing site and device information.
    """
    return perform_request_with_retries(f"{API_BASE_URL}/site-info/{site_id}")


def filter_relevant_outages(all_outages, site_info):
    """
    Filters outages based on the start date and device association with the site.

    Args:
        all_outages (list): The list of all outages retrieved.
        site_info (dict): The site information containing device details.

    Returns:
        list: A list of filtered outages associated with the site's devices.
    """
    if not site_info or 'devices' not in site_info:
        return []

    device_map = {device["id"]: device["name"] for device in site_info["devices"]}
    relevant_outages = []

    for outage in all_outages:
        outage_start = datetime.fromisoformat(outage["begin"].replace("Z", "+00:00"))
        if outage["id"] in device_map and outage_start >= datetime.fromisoformat(MIN_DATE.replace("Z", "+00:00")):
            relevant_outages.append({
                "id": outage["id"],
                "name": device_map[outage["id"]],
                "begin": outage["begin"],
                "end": outage["end"]
            })

    return relevant_outages


def post_filtered_outages(site_id, outages):
    """
    Sends the filtered outages to the specified site endpoint.

    Args:
        site_id (str): The ID of the site to post outages for.
        outages (list): The list of filtered outages to be posted.
    """
    result = perform_request_with_retries(f"{API_BASE_URL}/site-outages/{site_id}", method='post', data=outages)
    if result is not None:
        print("Successfully posted filtered outages.")
    else:
        print(f"Failed to post outages for {site_id} after retries.")


def main():
    """
    Main function orchestrating the data retrieval, filtering, and posting process.
    """
    outages = fetch_all_outages()
    if outages is None:
        print("Failed to fetch outages. Exiting.")
        return

    site_details = fetch_site_details(TARGET_SITE)
    if site_details is None:
        print("Failed to fetch site details. Exiting.")
        return

    filtered_outages = filter_relevant_outages(outages, site_details)
    post_filtered_outages(TARGET_SITE, filtered_outages)


if __name__ == "__main__":
    main()
