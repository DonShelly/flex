import os
from datetime import datetime

import requests

# Constants
API_KEY = os.getenv("KRAKENFLEX_API_KEY", "EltgJ5G8m44IzwE6UN2Y4B4NjPW77Zk6FJK3lL23")
API_BASE_URL = "https://api.krakenflex.systems/interview-tests-mock-api/v1"
TARGET_SITE = "norwich-pear-tree"
MIN_DATE = "2022-01-01T00:00:00.000Z"

# Headers for API requests
api_headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}


def fetch_all_outages():
    """
    Fetches all outage data from the outages endpoint.

    Returns:
        list: A list containing all outages as dictionaries.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/outages", headers=api_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve outages: {e}")
        return []


def fetch_site_details(site_id):
    """
    Retrieves information about a specific site, including device details.

    Args:
        site_id (str): The ID of the site to retrieve details for.

    Returns:
        dict: A dictionary containing site and device information.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/site-info/{site_id}", headers=api_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve site information for {site_id}: {e}")
        return {}


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
    try:
        response = requests.post(f"{API_BASE_URL}/site-outages/{site_id}", headers=api_headers, json=outages)
        response.raise_for_status()
        print("Successfully posted filtered outages.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to post outages for {site_id}: {e}")


def main():
    """
    Main function orchestrating the data retrieval, filtering, and posting process.
    """
    outages = fetch_all_outages()
    site_details = fetch_site_details(TARGET_SITE)
    filtered_outages = filter_relevant_outages(outages, site_details)
    post_filtered_outages(TARGET_SITE, filtered_outages)


if __name__ == "__main__":
    main()
