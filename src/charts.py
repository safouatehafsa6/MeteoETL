from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_weather(df, out_dir):
    """
    Generate weather charts and save them as PNG files.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing date, station, temperature, humidity,
        pressure and wind_speed columns.
    out_dir : str or pathlib.Path
        Directory where PNG charts will be saved.

    Returns
    -------
    list[pathlib.Path]
        Paths of the generated PNG files.
    """
    required_columns = {
        "date",
        "station",
        "temperature",
        "humidity",
        "pressure",
        "wind_speed",
    }

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df doit être un pandas DataFrame.")

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise ValueError(
            f"Colonnes manquantes : {', '.join(sorted(missing_columns))}"
        )

    if df.empty:
        raise ValueError("Le DataFrame est vide.")

    data = df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")

    metrics = {
        "temperature": {
            "title": "Evolution de la temperature",
            "ylabel": "Temperature (°C)",
            "filename": "temperature.png",
        },
        "humidity": {
            "title": "Evolution de l'humidite",
            "ylabel": "Humidite (%)",
            "filename": "humidite.png",
        },
        "pressure": {
            "title": "Evolution de la pression",
            "ylabel": "Pression (hPa)",
            "filename": "pression.png",
        },
        "wind_speed": {
            "title": "Evolution de la vitesse du vent",
            "ylabel": "Vitesse du vent",
            "filename": "vitesse_vent.png",
        },
    }

    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for column, config in metrics.items():
        chart_data = data.copy()
        chart_data[column] = pd.to_numeric(
            chart_data[column], errors="coerce"
        )

        chart_data = chart_data.dropna(subset=["date", column])

        if chart_data.empty:
            continue

        chart_data = chart_data.sort_values("date")

        fig, ax = plt.subplots(figsize=(10, 5))

        try:
            for station, station_data in chart_data.groupby(
                "station", dropna=False
            ):
                station_label = (
                    "Station inconnue" if pd.isna(station) else str(station)
                )

                ax.plot(
                    station_data["date"],
                    station_data[column],
                    marker="o",
                    label=station_label,
                )

            ax.set_title(config["title"])
            ax.set_xlabel("Date")
            ax.set_ylabel(config["ylabel"])
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend()
            fig.autofmt_xdate()
            fig.tight_layout()

            output_path = output_dir / config["filename"]
            fig.savefig(output_path, format="png", dpi=150)

            generated_files.append(output_path)

        finally:
            plt.close(fig)

    if not generated_files:
        raise ValueError("Aucune donnée météo valide pour générer les graphiques.")

    return generated_files
