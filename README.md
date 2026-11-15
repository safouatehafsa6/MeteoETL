"# MeteoETL" 

## Fonctionnalités

- **csv-ingest** : chargement des CSV météo et contrôle des colonnes (MASROUR Hafsa)

## Données

L'échantillon `data/sample/meteo_sample.csv` (5 villes marocaines, janvier-février 2026, un relevé toutes les 6 h) est téléchargé avec `scripts/fetch_sample.py` depuis l'API Open-Meteo (réanalyse ERA5).
Jeu complet : relancer le script avec d'autres dates (`START` / `END`) ou voir https://open-meteo.com/en/docs/historical-weather-api.
Source : Zippenfenig, P. (2023), Open-Meteo.com Weather API, Zenodo, DOI 10.5281/ZENODO.7970649.
