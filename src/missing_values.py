import pandas as pd

NUMERIC_COLS = ["temperature", "humidity", "pressure", "wind_speed"]


def handle_missing(df, strategy="mean"):
    """Traite les valeurs manquantes d'un DataFrame météo.

    strategy : "mean" (remplace par la moyenne de la station), "interpolate"
    (interpolation linéaire par station, dans l'ordre chronologique des
    dates) ou "drop" (supprime les lignes incomplètes). Le calcul se fait
    station par station.

    Une station qui n'a que des valeurs manquantes dans une colonne garde
    cette colonne vide avec "mean" et "interpolate" (on n'invente pas de
    données) ; utiliser "drop" pour supprimer ces lignes.

    Les lignes dont la station est manquante ne sont pas modifiées avec
    "mean" et "interpolate" (on ne sait pas à quelle station les rattacher).
    """
    df = df.copy()
    if df.empty:
        return df
    cols = [c for c in NUMERIC_COLS if c in df.columns]

    if strategy == "drop":
        return df.dropna(subset=cols).reset_index(drop=True)

    if strategy not in ("mean", "interpolate"):
        raise ValueError(f"Stratégie inconnue : {strategy}")

    original_index = df.index
    df = df.reset_index(drop=True)

    if strategy == "interpolate" and "date" in df.columns:
        # Interpolation dans l'ordre chronologique (tri stable)
        order = pd.to_datetime(df["date"], errors="coerce").sort_values(kind="stable").index
        work = df.loc[order]
    else:
        work = df

    if "station" in work.columns:
        known = work["station"].notna()
        groups = work.loc[known].groupby("station")[cols]
        if strategy == "mean":
            filled = groups.transform(lambda s: s.fillna(s.mean()))
        else:
            filled = groups.transform(
                lambda s: s.interpolate(method="linear", limit_direction="both")
            )
        work = work.copy()
        work.loc[known, cols] = filled
    else:
        work = work.copy()
        if strategy == "mean":
            work[cols] = work[cols].fillna(work[cols].mean())
        else:
            work[cols] = work[cols].interpolate(method="linear", limit_direction="both")

    # Retour à l'ordre et à l'index d'origine
    result = work.sort_index()
    result.index = original_index
    return result