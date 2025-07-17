import json
from typing import Dict, List, Optional
from pprint import pprint
import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def make_request(params: Dict) -> httpx.Response:
    res = httpx.get(GEOCODING_URL, params=params)
    res.raise_for_status()
    return res


def main() -> None:
    params = {
        "name": "Virginia Beach",
        "count": 10,
        "format": "json",
        "language": "en",
        "countryCode": "US",
    }
    res = json.loads(make_request(params=params).text)
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
