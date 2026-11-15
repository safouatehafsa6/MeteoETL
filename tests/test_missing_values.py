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


@pytest.mark.parametrize("strategy", ["mean", "interpolate", "drop"])
def test_no_nan_returns_unchanged(strategy):
    df = pd.DataFrame({
        "date": ["2026-01-01 00:00", "2026-01-01 06:00"],
        "station": ["Agadir", "Agadir"],
        "temperature": [10.0, 12.0],
        "humidity": [50.0, 55.0],
        "pressure": [1010.0, 1011.0],
        "wind_speed": [5.0, 6.0],
    })
    result = handle_missing(df, strategy)
    pd.testing.assert_frame_equal(result, df)


@pytest.mark.parametrize("strategy", ["mean", "interpolate"])
def test_station_with_only_nan_stays_empty(strategy):
    df = pd.DataFrame({
        "date": ["d1", "d2", "d3", "d4"],
        "station": ["Agadir", "Agadir", "Rabat", "Rabat"],
        "temperature": [None, None, 20.0, 22.0],
        "humidity": [50.0, 60.0, 70.0, 80.0],
        "pressure": [1010.0, 1012.0, 1014.0, 1016.0],
        "wind_speed": [5.0, 6.0, 7.0, 8.0],
    })
    result = handle_missing(df, strategy)
    assert result.loc[result["station"] == "Agadir", "temperature"].isna().all()
    assert result.loc[result["station"] == "Rabat", "temperature"].notna().all()


@pytest.mark.parametrize("strategy", ["mean", "interpolate", "drop"])
def test_empty_dataframe(strategy):
    df = pd.DataFrame(columns=["date", "station", "temperature",
                               "humidity", "pressure", "wind_speed"])
    result = handle_missing(df, strategy)
    assert result.empty