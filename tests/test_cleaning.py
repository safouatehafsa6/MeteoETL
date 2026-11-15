import pandas as pd
from src.cleaning import clean


def make_df():
    return pd.DataFrame({
        "date": ["2026-01-01 00:00", "2026-01-01 00:00",
                 "2026-01-01 06:00", "2026-01-01 12:00"],
        "station": ["Casablanca"] * 4,
        "temperature": [13.1, 13.1, 14.0, 120.0],
        "humidity": [82, 82, 80, 75],
        "pressure": [1019.6, 1019.6, 1018.0, 1017.0],
        "wind_speed": [9.4, 9.4, 10.0, 8.0],
    })


def test_duplicates_removed():
    result = clean(make_df())
    assert result.duplicated().sum() == 0


def test_impossible_temperature_removed():
    result = clean(make_df())
    assert result["temperature"].max() <= 60


def test_date_is_datetime():
    result = clean(make_df())
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_negative_wind_removed():
    df = make_df()
    df.loc[2, "wind_speed"] = -5
    result = clean(df)
    assert (result["wind_speed"] >= 0).all()