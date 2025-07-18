"""This module provides a script to test the Historic Weather API"""

from typing import Dict
import pandas as pd

from historic import make_request


def parse_single_hourly(hourly, keys: Dict, search_key: str):
    return hourly.Variables(*[k for k in keys if keys[k] == search_key]).ValuesAsNumpy()


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
        9: "wind_speed_10m",
        10: "wind_speed_100m",
        11: "wind_direction_10m",
        12: "wind_direction_100m",
        13: "wind_gusts_10m",
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

    hour_df["temperature_2m"] = parse_single_hourly(
        hourly, hourly_keys, "temperature_2m"
    )
    hour_df["dewpoint_2m"] = parse_single_hourly(hourly, hourly_keys, "dewpoint_2m")

    hour_df["apparent_temperature"] = parse_single_hourly(
        hourly, hourly_keys, "apparent_temperature"
    )
    hour_df["sealevel_pressure"] = parse_single_hourly(
        hourly, hourly_keys, "pressure_msl"
    )
    hour_df["surface_pressure"] = parse_single_hourly(
        hourly, hourly_keys, "surface_pressure"
    )
    hour_df["precipitation"] = parse_single_hourly(hourly, hourly_keys, "precipitation")
    hour_df["rain"] = parse_single_hourly(hourly, hourly_keys, "rain")
    hour_df["snowfall"] = parse_single_hourly(hourly, hourly_keys, "snowfall")
    hour_df["snow_depth"] = parse_single_hourly(hourly, hourly_keys, "snow_depth")
    hour_df["wind_speed_10m"] = parse_single_hourly(
        hourly, hourly_keys, "wind_speed_10m"
    )
    hour_df["wind_speed_100m"] = parse_single_hourly(
        hourly, hourly_keys, "wind_speed_100m"
    )
    hour_df["wind_direction_10m"] = parse_single_hourly(
        hourly, hourly_keys, "wind_direction_10m"
    )
    hour_df["wind_direction_100m"] = parse_single_hourly(
        hourly, hourly_keys, "wind_direction_100m"
    )
    hour_df["wind_gusts_10m"] = parse_single_hourly(
        hourly, hourly_keys, "wind_gusts_10m"
    )

    hour_df = pd.DataFrame(data=hour_df)
    hour_df.to_csv("vb.csv", index=False)
    print("Data saved to csv")


if __name__ == "__main__":
    main()
