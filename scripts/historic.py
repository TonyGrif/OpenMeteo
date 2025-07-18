"""This module provides a script to test the Historic Weather API"""

import sqlite3

import pandas as pd

from historic import make_request


def main() -> None:
    """Main Script and entry point of this module"""
    hourly_keys = {
        0: "temperature_2m",
        1: "dewpoint_2m",
        2: "apparent_temperature",
        3: "pressure_msl",
        4: "surface_pressure",
        5: "precipitation",
        6: "rain",
        7: "snowfall",
        8: "snow_depth",
    }

    # TODO: Allow passing this in via CLI
    params = {
        "latitude": 36.85293,
        "longitude": -75.97799,
        "start_date": "2000-01-01",
        "end_date": "2025-07-15",
        "hourly": list(hourly_keys.values()),
    }

    res = make_request(params=params)

    hourly = res[0].Hourly()
    hour_df = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    # TODO: This is nasty and reused code hello, fix this pls
    hour_df["temperature_2m"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "temperature_2m"]
    ).ValuesAsNumpy()

    hour_df["dewpoint_2m"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "dewpoint_2m"]
    ).ValuesAsNumpy()

    hour_df["apparent_temperature"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "apparent_temperature"]
    ).ValuesAsNumpy()

    hour_df["sealevel_pressure"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "pressure_msl"]
    ).ValuesAsNumpy()

    hour_df["surface_pressure"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "surface_pressure"]
    ).ValuesAsNumpy()

    hour_df["precipitation"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "precipitation"]
    ).ValuesAsNumpy()

    hour_df["rain"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "rain"]
    ).ValuesAsNumpy()

    hour_df["snowfall"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "snowfall"]
    ).ValuesAsNumpy()

    hour_df["snow_depth"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "snow_depth"]
    ).ValuesAsNumpy()

    hour_df = pd.DataFrame(data=hour_df)

    con = sqlite3.connect("vb.db")
    hour_df.to_sql("hourly", con)
    print("Data saved to db")


if __name__ == "__main__":
    main()
