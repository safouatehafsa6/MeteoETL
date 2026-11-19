from pathlib import Path

import pandas as pd
import pytest
from src.daily_aggregates import compute_daily

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "meteo_sample.csv"


def make_df():
    return pd.DataFrame({
        "date": ["2026-01-01 06:00", "2026-01-01 12:00", "2026-01-02 06:00"],
        "station": ["Agadir", "Agadir", "Agadir"],
        "temperature": [10.0, 20.0, 15.0],
        "humidity": [50.0, 70.0, 60.0],
        "pressure": [1010.0, 1012.0, 1011.0],
        "wind_speed": [5.0, 15.0, 10.0],
    })


def test_min_max_mean_per_day():
    result = compute_daily(make_df())
    assert len(result) == 2  # 2 jours -> 2 lignes
    day1 = result.iloc[0]
    assert day1["temperature_min"] == 10.0
    assert day1["temperature_max"] == 20.0
    assert day1["temperature_mean"] == 15.0
    assert day1["wind_speed_max"] == 15.0


def test_aggregation_is_per_station():
    df = pd.DataFrame({
        "date": ["2026-01-01 00:00", "2026-01-01 00:00",
                 "2026-01-01 06:00", "2026-01-01 06:00"],
        "station": ["Agadir", "Rabat", "Agadir", "Rabat"],
        "temperature": [10.0, 30.0, 20.0, 40.0],
        "humidity": [50.0, 60.0, 70.0, 80.0],
        "pressure": [1010.0, 1015.0, 1012.0, 1017.0],
        "wind_speed": [5.0, 6.0, 7.0, 8.0],
    })
    result = compute_daily(df)
    assert len(result) == 2
    agadir = result[result["station"] == "Agadir"].iloc[0]
    rabat = result[result["station"] == "Rabat"].iloc[0]
    assert agadir["temperature_mean"] == 15.0
    assert rabat["temperature_mean"] == 35.0


def test_missing_values_are_ignored():
    df = make_df()
    df.loc[1, "temperature"] = None  # reste seulement 10.0 le 1er janvier
    result = compute_daily(df)
    assert result.iloc[0]["temperature_mean"] == 10.0


def test_missing_column_raises():
    with pytest.raises(ValueError):
        compute_daily(make_df().drop(columns=["pressure"]))


def test_empty_dataframe():
    df = pd.DataFrame(columns=["date", "station", "temperature",
                               "humidity", "pressure", "wind_speed"])
    result = compute_daily(df)
    assert result.empty
    assert "temperature_min" in result.columns


def test_does_not_modify_input():
    df = make_df()
    before = df.copy()
    compute_daily(df)
    pd.testing.assert_frame_equal(df, before)


def test_on_sample_data():
    df = pd.read_csv(SAMPLE)
    result = compute_daily(df)
    n_days = pd.to_datetime(df["date"]).dt.normalize().nunique()
    assert len(result) == n_days * df["station"].nunique()
    assert (result["temperature_min"] <= result["temperature_mean"]).all()
    assert (result["temperature_mean"] <= result["temperature_max"]).all()