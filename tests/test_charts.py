import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from src.charts import plot_weather


@pytest.fixture
def weather_data():
    return pd.DataFrame({
        "date": [
            "2026-01-01",
            "2026-01-02",
            "2026-01-01",
            "2026-01-02",
        ],
        "station": [
            "Casablanca",
            "Casablanca",
            "Rabat",
            "Rabat",
        ],
        "temperature": [18, 20, 16, 19],
        "humidity": [70, 65, 75, 68],
        "pressure": [1012, 1013, 1010, 1011],
        "wind_speed": [12, 15, 10, 13],
    })


def test_plot_weather_creates_four_png_files(weather_data, tmp_path):
    files = plot_weather(weather_data, tmp_path)

    assert len(files) == 4

    for file_path in files:
        assert file_path.exists()
        assert file_path.suffix == ".png"
        assert file_path.stat().st_size > 0


def test_plot_weather_creates_output_directory(weather_data, tmp_path):
    output_dir = tmp_path / "charts"

    plot_weather(weather_data, output_dir)

    assert output_dir.exists()
    assert (output_dir / "temperature.png").exists()


def test_plot_weather_handles_missing_values(weather_data, tmp_path):
    weather_data.loc[0, "temperature"] = None

    files = plot_weather(weather_data, tmp_path)

    assert len(files) == 4


def test_plot_weather_skips_metric_without_valid_values(
    weather_data, tmp_path
):
    weather_data["humidity"] = None

    files = plot_weather(weather_data, tmp_path)

    assert len(files) == 3
    assert not (tmp_path / "humidite.png").exists()


def test_plot_weather_raises_error_for_empty_dataframe(tmp_path):
    columns = [
        "date",
        "station",
        "temperature",
        "humidity",
        "pressure",
        "wind_speed",
    ]

    df = pd.DataFrame(columns=columns)

    with pytest.raises(ValueError, match="vide"):
        plot_weather(df, tmp_path)


def test_plot_weather_raises_error_for_missing_columns(tmp_path):
    df = pd.DataFrame({
        "date": ["2026-01-01"],
        "station": ["Casablanca"],
    })

    with pytest.raises(ValueError, match="Colonnes manquantes"):
        plot_weather(df, tmp_path)


def test_plot_weather_rejects_invalid_input(tmp_path):
    with pytest.raises(TypeError):
        plot_weather([], tmp_path)
