import pandas as pd
from src.cleaning import drop_duplicates

def test_drop_duplicates():
    df = pd.DataFrame({
        "temperature": [20, 20, 25]
    })

    result = drop_duplicates(df)

    assert len(result) == 2

def test_empty_dataframe():
    df = pd.DataFrame()

    result = drop_duplicates(df)

    assert result.empty