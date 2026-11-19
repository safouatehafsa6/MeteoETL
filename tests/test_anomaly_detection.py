from pathlib import Path
import pandas as pd
import pytest

from src.anomaly_detection import detect_anomalies


def _sample_weather_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=8, freq="D"),
            "station": ["Casa"] * 8,
            "temperature": [18.0, 19.0, 17.5, 18.5, 19.2, 18.1, 17.8, 65.0],
            "humidity": [60, 62, 58, 61, 59, 63, 60, 61],
            "pressure": [1015, 1016, 1014, 1015, 1017, 1015, 1016, 1015],
            "wind_speed": [12.0, 14.0, 11.0, 13.0, 15.0, 12.5, 13.5, 14.0],
        }
    )


def test_detect_anomalies_iqr_flags_extreme_temperature():
    df = _sample_weather_df()
    out = detect_anomalies(df, threshold=1.5, method="iqr")

    assert "is_anomaly" in out.columns
    assert out["is_anomaly"].dtype == bool
    assert bool(out.loc[out.index[-1], "is_anomaly"]) is True
    assert out["is_anomaly"].iloc[:-1].sum() == 0


def test_detect_anomalies_zscore_method():
    df = _sample_weather_df()
    out = detect_anomalies(df, threshold=2.0, method="zscore")

    assert "is_anomaly" in out.columns
    assert bool(out.loc[out.index[-1], "is_anomaly"]) is True


def test_detect_anomalies_empty_dataframe():
    empty_df = pd.DataFrame(
        columns=["date", "station", "temperature", "humidity", "pressure", "wind_speed"]
    )
    out = detect_anomalies(empty_df, threshold=1.5)

    assert out.empty
    assert "is_anomaly" in out.columns


def test_detect_anomalies_invalid_threshold():
    df = _sample_weather_df()
    with pytest.raises(ValueError):
        detect_anomalies(df, threshold=0)


def test_detect_anomalies_on_sample_csv_if_present():
    sample_files = list(Path("data/sample").glob("*.csv"))
    if not sample_files:
        pytest.skip("Aucun fichier CSV trouvé dans data/sample/")

    df = pd.read_csv(sample_files[0])
    out = detect_anomalies(df, threshold=1.5)
    assert "is_anomaly" in out.columns
    assert len(out) == len(df)