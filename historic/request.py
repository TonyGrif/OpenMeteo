"""This module provides methods to make a request on the Historical Weather API"""

from typing import Dict, List

import openmeteo_requests

HISTORIC_URL = "https://archive-api.open-meteo.com/v1/archive"


def make_request(params: Dict) -> List:
    """Make a request on the Historical Weather API

    Args:
        params: Parameters for the API; this **must** contain longitude (float),
        latitude (float), start_date (str), and end_date (str) keys; variables are
        queried through specified keys (i.e: daily values use the "daily" key
        and hourly values use the "hourly" key), these values are a list of
        strings

    Returns:
        TBW

    Throws:
        OpenMeteoRequestsError on bad status codes
    """
    om = openmeteo_requests.Client()
    return om.weather_api(HISTORIC_URL, params=params)
