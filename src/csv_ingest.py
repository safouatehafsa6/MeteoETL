import pandas as pd

EXPECTED_COLUMNS = ["date", "station", "temperature", "humidity", "pressure", "wind_speed"]


def load_csv(path):
    """Charge un CSV météo brut et vérifie que les colonnes attendues sont présentes."""
    df = pd.read_csv(path)
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")
    if df.empty:
        raise ValueError("Le fichier CSV ne contient aucune ligne")
    return df[EXPECTED_COLUMNS]
