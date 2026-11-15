import pandas as pd
from src.anomaly_detection import detect_anomalies

def test_detect_anomalies():
    data = {
        "date": ["2026-06-01", "2026-06-02", "2026-06-03"],
        "station": ["A", "A", "A"],
        "temperature": [22.5, 23.0, 65.0],
        "humidity": [50, 52, 49],
        "pressure": [1013, 1012, 1010],
        "wind_speed": [10, 12, 15]
    }
    df = pd.DataFrame(data)
    
    result_df = detect_anomalies(df, threshold=1.0)
    
    assert "is_anomaly" in result_df.columns
    assert result_df.iloc[2]["is_anomaly"] == True