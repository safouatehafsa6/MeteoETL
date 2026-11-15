import sqlite3
import pandas as pd
import pytest
from src.sqlite_load import save_to_sqlite


def test_save_to_sqlite_ok(tmp_path):
    df = pd.DataFrame(
        {
            "date": ["2026-01-01", "2026-01-02"],
            "station": ["Casablanca", "Rabat"],
            "temperature": [18.5, 19.2],
            "humidity": [70.0, 65.0],
            "pressure": [1015.0, 1016.0],
            "wind_speed": [12.0, 10.5],
        }
    )
    db_file = tmp_path / "meteo.db"

    rows = save_to_sqlite(df, str(db_file), "meteo_daily")

    assert rows == 2
    assert db_file.exists()

    with sqlite3.connect(db_file) as conn:
        loaded = pd.read_sql_query("SELECT * FROM meteo_daily", conn)

    assert len(loaded) == 2
    assert list(loaded["station"]) == ["Casablanca", "Rabat"]
def test_save_to_sqlite_empty_raises(tmp_path):
    df = pd.DataFrame()
    with pytest.raises(ValueError):
        save_to_sqlite(df, str(tmp_path / "empty.db"), "meteo_daily")