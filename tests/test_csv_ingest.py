import pandas as pd
import pytest

from src.csv_ingest import load_csv, EXPECTED_COLUMNS

SAMPLE = "data/sample/meteo_sample.csv"


def test_load_csv_ok():
    df = load_csv(SAMPLE)
    assert list(df.columns) == EXPECTED_COLUMNS
    assert len(df) > 1000


def test_sample_has_five_stations():
    assert load_csv(SAMPLE)["station"].nunique() == 5


def test_sample_values_are_plausible():
    df = load_csv(SAMPLE)
    assert df["temperature"].between(-10, 50).all()
    assert df["humidity"].between(0, 100).all()
    assert df["pressure"].between(800, 1100).all()


def test_load_csv_missing_column(tmp_path):
    bad = tmp_path / "bad.csv"
    pd.DataFrame({"date": ["2026-01-01"]}).to_csv(bad, index=False)
    with pytest.raises(ValueError):
        load_csv(str(bad))


def test_load_csv_empty_file(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text(",".join(EXPECTED_COLUMNS) + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_csv(str(empty))


def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("data/sample/inexistant.csv")
