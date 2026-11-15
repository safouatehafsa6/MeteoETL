import pandas as pd

NUMERIC_COLUMNS = ["temperature", "humidity", "pressure", "wind_speed"]


def clean(df):
    df = df.copy()

    # 1. supprimer les doublons
    df = df.drop_duplicates()

    # 2. convertir "date" en vraie date (dates invalides supprimées)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # 3. convertir les colonnes en nombres
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4. retirer les valeurs aberrantes évidentes (les NaN sont gardés)
    df = df[df["temperature"].between(-50, 60) | df["temperature"].isna()]
    df = df[df["humidity"].between(0, 100) | df["humidity"].isna()]
    df = df[df["wind_speed"].ge(0) | df["wind_speed"].isna()]

    return df.reset_index(drop=True)