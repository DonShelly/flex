import requests

API_KEY = "your_default_api_key"
API_BASE_URL = "https://api.krakenflex.systems/interview-tests-mock-api/v1"

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
