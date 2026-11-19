"""Télécharge un échantillon de vraies données météo (Open-Meteo, archive ERA5)
et écrit data/sample/meteo_sample.csv (5 villes, 60 jours, un relevé toutes les 6 h)."""
import csv
import json
import urllib.request

STATIONS = {
    "Casablanca": (33.57, -7.59),
    "Rabat": (34.02, -6.84),
    "Marrakech": (31.63, -8.01),
    "Tanger": (35.76, -5.83),
    "Agadir": (30.43, -9.60),
}
START, END = "2026-01-01", "2026-02-28"
URL = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude={lat}&longitude={lon}&start_date={s}&end_date={e}"
    "&hourly=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m"
    "&timezone=Africa%2FCasablanca"
)

rows = []
for station, (lat, lon) in STATIONS.items():
    url = URL.format(lat=lat, lon=lon, s=START, e=END)
    with urllib.request.urlopen(url, timeout=60) as resp:
        h = json.load(resp)["hourly"]
    for i, t in enumerate(h["time"]):
        if i % 6 != 0:          # un relevé toutes les 6 h pour rester léger
            continue
        rows.append([
            t.replace("T", " "),
            station,
            h["temperature_2m"][i],
            h["relative_humidity_2m"][i],
            h["surface_pressure"][i],
            h["wind_speed_10m"][i],
        ])

rows.sort(key=lambda r: (r[0], r[1]))
with open("data/sample/meteo_sample.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["date", "station", "temperature", "humidity", "pressure", "wind_speed"])
    w.writerows(rows)
print(f"{len(rows)} lignes écrites")
