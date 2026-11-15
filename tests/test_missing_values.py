import pandas as pd
import pytest
from src.missing_values import handle_missing


def make_df():
    return pd.DataFrame({
        "date": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "station": ["A", "A", "A"],
        "temperature": [10.0, None, 20.0],
        "humidity": [50.0, 60.0, 70.0],
        "pressure": [1010.0, 1012.0, 1014.0],
        "wind_speed": [5.0, 6.0, 7.0],
    })


def make_two_stations():
    return pd.DataFrame({
        "date": ["2026-01-01 00:00", "2026-01-01 00:00",
                 "2026-01-01 06:00", "2026-01-01 06:00",
                 "2026-01-01 12:00", "2026-01-01 12:00"],
        "station": ["Agadir", "Casablanca"] * 3,
        "temperature": [10.0, 30.0, None, 32.0, 20.0, 34.0],
        "humidity": [50, 60, 55, 62, 60, 64],
        "pressure": [1010.0, 1015.0, 1011.0, 1016.0, 1012.0, 1017.0],
        "wind_speed": [5.0, 6.0, 5.5, 6.5, 6.0, 7.0],
    })


def test_mean_fills_missing():
    result = handle_missing(make_df(), "mean")
    assert result["temperature"].isna().sum() == 0
    assert result["temperature"][1] == 15.0


def test_interpolate_fills_missing():
    result = handle_missing(make_df(), "interpolate")
    assert result["temperature"][1] == 15.0


def test_drop_removes_rows():
    result = handle_missing(make_df(), "drop")
    assert len(result) == 2


def test_unknown_strategy_raises():
    with pytest.raises(ValueError):
        handle_missing(make_df(), "nimporte-quoi")


def test_mean_is_computed_per_station():
    result = handle_missing(make_two_stations(), "mean")
    assert result.loc[2, "temperature"] == 15.0


def test_interpolate_is_computed_per_station():
    result = handle_missing(make_two_stations(), "interpolate")
    assert result.loc[2, "temperature"] == 15.0