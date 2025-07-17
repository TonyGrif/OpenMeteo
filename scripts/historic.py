"""This module provides a script to test the Historic Weather API"""

import sqlite3
from pprint import pprint

import pandas as pd

from historic import make_request


def main() -> None:
    """Main Script and entry point of this module"""
    hourly_keys = {0: "temperature_2m"}

    # TODO: Allow passing this in via CLI
    params = {
        "latitude": 36.85293,
        "longitude": -75.97799,
        "start_date": "2025-07-01",
        "end_date": "2025-07-16",
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

    hour_df["temperature_2m"] = hourly.Variables(
        *[k for k in hourly_keys if hourly_keys[k] == "temperature_2m"]
    ).ValuesAsNumpy()

    pprint(hour_df["temperature_2m"])

    hour_df = pd.DataFrame(data=hour_df)

    con = sqlite3.connect("temperatures.db")
    hour_df.to_sql("vb", con)


if __name__ == "__main__":
    main()
