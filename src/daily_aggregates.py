import pandas as pd

NUMERIC_COLS = ["temperature", "humidity", "pressure", "wind_speed"]
STATS = ["min", "max", "mean"]


def compute_daily(df):
    """Calcule les statistiques journalières d'un DataFrame météo.

    Pour chaque couple (jour, station), renvoie le min, le max et la
    moyenne de chaque variable numérique. Les colonnes du résultat sont
    nommées <variable>_min, <variable>_max et <variable>_mean
    (ex. temperature_min).

    Les valeurs manquantes sont ignorées dans le calcul. Les lignes dont la
    date est invalide ou dont la station est manquante sont écartées (on ne
    sait pas à quel groupe les rattacher). Le résultat est trié par date
    puis par station.
    """
    required = ["date", "station"] + NUMERIC_COLS
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    columns = ["date", "station"] + [f"{c}_{s}" for c in NUMERIC_COLS for s in STATS]
    if df.empty:
        return pd.DataFrame(columns=columns)

    data = df.copy()
    # normalize() ramène "2026-01-01 06:00" à "2026-01-01" : un groupe par jour
    data["date"] = pd.to_datetime(data["date"], errors="coerce").dt.normalize()

    daily = data.groupby(["date", "station"])[NUMERIC_COLS].agg(STATS)
    daily.columns = [f"{col}_{stat}" for col, stat in daily.columns]
    return daily.reset_index()