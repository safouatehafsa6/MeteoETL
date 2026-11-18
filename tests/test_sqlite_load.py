
import sqlite3
import pandas as pd
import pytest

from src.sqlite_load import save_to_sqlite


def test_save_to_sqlite(tmp_path):
    df = pd.DataFrame({
        "date": ["2026-11-16", "2026-11-17"],
        "station": ["Casablanca", "Rabat"],
        "temperature": [22, 24],
        "humidity": [60, 55],
        "pressure": [1012, 1013],
        "wind_speed": [12, 15],
    })

    db_path = tmp_path / "meteo.db"

    result = save_to_sqlite(df, str(db_path))

    assert result == 2

    with sqlite3.connect(db_path) as conn:
        saved = pd.read_sql("SELECT * FROM meteo", conn)

    assert len(saved) == 2


def test_empty_dataframe(tmp_path):
    df = pd.DataFrame()
    db_path = tmp_path / "meteo.db"

    with pytest.raises(ValueError, match="DataFrame est vide"):
        save_to_sqlite(df, str(db_path))


def test_missing_required_columns(tmp_path):
    df = pd.DataFrame({
        "date": ["2026-11-17"],
        "temperature": [22],
    })

    db_path = tmp_path / "meteo.db"

    with pytest.raises(ValueError, match="Colonnes manquantes"):
        save_to_sqlite(df, str(db_path))


def test_append_preserves_existing_data(tmp_path):
    db_path = tmp_path / "meteo.db"

    old_data = pd.DataFrame({
        "date": ["2026-11-16"],
        "station": ["Casablanca"],
        "temperature": [22],
        "humidity": [60],
        "pressure": [1012],
        "wind_speed": [12],
    })

    new_data = pd.DataFrame({
        "date": ["2026-11-17"],
        "station": ["Rabat"],
        "temperature": [24],
        "humidity": [55],
        "pressure": [1013],
        "wind_speed": [15],
    })

    save_to_sqlite(old_data, str(db_path))
    save_to_sqlite(new_data, str(db_path))

    with sqlite3.connect(db_path) as conn:
        saved = pd.read_sql("SELECT * FROM meteo", conn)

    assert len(saved) == 2
    assert set(saved["station"]) == {"Casablanca", "Rabat"}
