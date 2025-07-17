"""This module provides a script to test the Geocoding API"""

import json
from pprint import pprint
from typing import Dict, List, Optional

from geocoding import make_request


def main() -> None:
    """Main script and entry point for this module"""
    # TODO: Allow passing this in via CLI
    params = {
        "name": "Virginia Beach",
        "count": 10,
        "format": "json",
        "language": "en",
        "countryCode": "US",
    }

    res = json.loads(make_request(params=params).text)

    # TODO: Create some filtering methods, for resuse
    data = [entry for entry in res["results"] if entry["admin1"] == "Virginia"]

    save_keys = ["latitude", "longitude", "name"]
    filtered_data: List[Dict] = []

    for value in data:
        filtered_data.append({key: value[key] for key in save_keys})

    pprint(filtered_data)

    filename = "geocodes.json"
    with open(filename, "w") as file:
        json.dump(filtered_data, file)
    print(f"Geocodes saved to {filename}")


if __name__ == "__main__":
    main()
