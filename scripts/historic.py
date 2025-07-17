"""This module provides a script to test the Historic Weather API"""

from pprint import pprint

from historic import make_request


def main() -> None:
    """Main Script and entry point of this module"""
    # TODO: Allow passing this in via CLI
    params = {
        "latitude": 36.85293,
        "longitude": -75.97799,
        "start_date": "2025-07-01",
        "end_date": "2025-07-16",
        "hourly": [
            "temperature_2m",
            "temperature_80m",
            "temperature_120m",
            "temperature_180m",
            "pressure_msl",
            "surface_pressure",
            "dew_point_2m",
        ],
    }

    res = make_request(params=params)
    pprint(res)


if __name__ == "__main__":
    main()
