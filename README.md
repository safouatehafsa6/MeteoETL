# MeteoETL

Pipeline de données météo (Python : pandas, matplotlib, pytest).

## Fonctionnalités

- **Configuration YAML** : lecture des paramètres du pipeline (`src/config.py`) — *Soukaina*
- **cleaning** : nettoyage des données (TAIR Zahra)
feature/charts
- **Charts météo** : génération de graphiques PNG pour visualiser l'évolution de la température, de l'humidité, de la pression et de la vitesse du vent par station — Zineb (équipe E3).
- **missing-values** : traitement des valeurs manquantes (AOUZAL Salma)
-  develop
- **csv-ingest** : chargement des CSV météo et contrôle des colonnes (MASROUR Hafsa)

## Données

L'échantillon `data/sample/meteo_sample.csv` (5 villes marocaines, janvier-février 2026, un relevé toutes les 6 h) est téléchargé avec `scripts/fetch_sample.py` depuis l'API Open-Meteo (réanalyse ERA5).
Jeu complet : relancer le script avec d'autres dates (`START` / `END`) ou voir https://open-meteo.com/en/docs/historical-weather-api.
Source : Zippenfenig, P. (2023), Open-Meteo.com Weather API, Zenodo, DOI 10.5281/ZENODO.7970649.
