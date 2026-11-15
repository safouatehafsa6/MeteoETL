import sqlite3
from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "station",
    "temperature",
    "humidity",
    "pressure",
    "wind_speed",
]


def save_to_sqlite(df: pd.DataFrame, db_path: str, table: str = "meteo") -> int:
    """Sauvegarde un DataFrame météo dans une table SQLite et retourne le nombre de lignes."""
    if df is None or df.empty:
        raise ValueError("Le DataFrame est vide, aucune donnée à sauvegarder.")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)

    return len(df)