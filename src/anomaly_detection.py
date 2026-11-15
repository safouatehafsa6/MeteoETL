import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame, threshold: float = 3.0) -> pd.DataFrame:
    df = df.copy()
    
    if "temperature" not in df.columns or df.empty:
        df["is_anomaly"] = False
        return df

    mean_val = df["temperature"].mean()
    std_val = df["temperature"].std()
    
    if std_val == 0 or pd.isna(std_val):
        df["is_anomaly"] = False
        return df

    z_scores = np.abs((df["temperature"] - mean_val) / std_val)
    df["is_anomaly"] = z_scores > threshold
    
    return df