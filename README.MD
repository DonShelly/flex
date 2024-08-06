# Outage Management System

## Overview

The Outage Management System is a Python application designed to interact with the KrakenFlex API to manage and report outages. It retrieves outage data, filters relevant outages based on specific criteria, and reports these outages to the appropriate endpoint.

## Features

- **Fetch Outages**: Retrieve all outages from the KrakenFlex API.
- **Fetch Site Details**: Obtain site information, including device details.
- **Filter Outages**: Select relevant outages based on date and device association.
- **Post Outages**: Report filtered outages to a specified site endpoint.
- **Resilience to Errors**: Implements a retry mechanism with exponential backoff for handling server errors (HTTP 500).

## Project Structure
```python
project/
    ├── main.py # Core application logic
    ├── requirements.txt # Python dependencies
    ├── test.py # python test cases
    └── .gitignore # Git ignore file for Python
```
       

## Getting Started

### Prerequisites

- Python 3.7+
- Virtual environment tool (optional but recommended)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   
2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
4. **Set Up Environment Variables:**

- Create a .env file in the project root directory (if not using environment variables directly) and add your API key:
makefile
  ```bash
  KRAKENFLEX_API_KEY=your_api_key_here


## How It Works
1. Fetches Outages: The system retrieves all outages from the /outages endpoint.
2. Fetches Site Information: Retrieves details for the specified site from the /site-info/{site_id} endpoint.
3. Filters Relevant Outages: Outages that started before 2022-01-01T00:00:00.000Z or do not correspond to devices in the site information are filtered out.
4. Posts Filtered Outages: The filtered outages are then posted to the /site-outages/{site_id} endpoint.

## Error Handling
The application includes a retry mechanism for API requests, which retries up to five times with an exponential backoff strategy in case of HTTP 500 errors. This ensures the system can handle temporary server issues gracefully.

# Testing
Unit tests are implemented to validate the functionality of each component. To run the tests, execute the following command:

```bash
    python -m unittest discover
