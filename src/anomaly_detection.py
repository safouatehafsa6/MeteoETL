from __future__ import annotations

import numpy as np
import pandas as pd

DEFAULT_NUMERIC_COLUMNS = ["temperature", "humidity", "pressure", "wind_speed"]


def detect_anomalies(
    df: pd.DataFrame,
    threshold: float = 1.5,
    method: str = "iqr",
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """Detect anomalous weather rows using IQR or Z-score and add an `is_anomaly` column."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")
    if threshold <= 0:
        raise ValueError("threshold must be strictly positive.")

    result = df.copy()
    if result.empty:
        result["is_anomaly"] = pd.Series(dtype=bool, index=result.index)
        return result

    target_cols = columns if columns is not None else [
        col for col in DEFAULT_NUMERIC_COLUMNS if col in result.columns
    ]
    if not target_cols:
        target_cols = list(result.select_dtypes(include=[np.number]).columns)

    anomaly_mask = pd.Series(False, index=result.index, dtype=bool)
    norm_method = method.lower()

    for col in target_cols:
        series = pd.to_numeric(result[col], errors="coerce")
        valid = series.dropna()
        if valid.empty:
            continue

        if norm_method == "iqr":
            q1 = valid.quantile(0.25)
            q3 = valid.quantile(0.75)
            iqr = q3 - q1
            if iqr == 0:
                continue
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
            col_anomalies = (series < lower) | (series > upper)
        elif norm_method == "zscore":
            std = valid.std(ddof=0)
            if std == 0:
                continue
            mean = valid.mean()
            z_scores = ((series - mean) / std).abs()
            col_anomalies = z_scores > threshold
        else:
            raise ValueError("method must be 'iqr' or 'zscore'.")

        anomaly_mask = anomaly_mask | col_anomalies.fillna(False)

    result["is_anomaly"] = anomaly_mask
    return result