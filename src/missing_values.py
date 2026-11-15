import pandas as pd

NUMERIC_COLS = ["temperature", "humidity", "pressure", "wind_speed"]


def handle_missing(df, strategy="mean"):
    """Traite les valeurs manquantes d'un DataFrame météo.

    strategy : "mean" (remplace par la moyenne de la station), "interpolate"
    (interpolation linéaire par station) ou "drop" (supprime les lignes
    incomplètes). Le calcul se fait station par station.
    """
    df = df.copy()
    cols = [c for c in NUMERIC_COLS if c in df.columns]

    if strategy == "drop":
        return df.dropna(subset=cols).reset_index(drop=True)

    if strategy not in ("mean", "interpolate"):
        raise ValueError(f"Stratégie inconnue : {strategy}")

    if "station" in df.columns:
        groups = df.groupby("station")[cols]
    else:
        groups = None

    if strategy == "mean":
        if groups is not None:
            df[cols] = groups.transform(lambda s: s.fillna(s.mean()))
        else:
            df[cols] = df[cols].fillna(df[cols].mean())
    else:
        if groups is not None:
            df[cols] = groups.transform(
                lambda s: s.interpolate(method="linear", limit_direction="both")
            )
        else:
            df[cols] = df[cols].interpolate(method="linear", limit_direction="both")

    return df