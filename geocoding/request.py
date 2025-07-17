"""This module provides methods to make a request on the Geocoding API"""

from typing import Dict

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def make_request(params: Dict) -> httpx.Response:
    """Make a request on the Geocoding API

    Args:
        params: Parameters for the API; this **must** contain a name key
        that contains at least 2 character (exact match locations) or at least
        3 characters (fuzzy matching)

    Returns:
        A HTTP response

    Throws:
        httpx.HTTPError on a request/status error
    """
    if (name := params.get("name")) is None:
        raise ValueError("Name key is required for this API")
    elif len(name) <= 1:
        raise ValueError("Name key must be greater than 1 character")

    res = httpx.get(GEOCODING_URL, params=params)
    res.raise_for_status()
    return res
