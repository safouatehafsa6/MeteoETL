# 🌦️ MeteoETL — Pipeline de Données Météorologiques

**Version actuelle : v1.0.0**

## 📋 Description du projet

**MeteoETL** est un pipeline de traitement de données météorologiques développé en Python dans le cadre du module **Outils DevOps** (Master Big Data et Cloud Computing - FS Aïn Chock).

Ce pipeline modulaire permet de :
1. **Ingérer** des relevés météorologiques bruts au format CSV.
2. **Nettoyer** les données (doublons, typage, formats de dates, valeurs aberrantes).
3. **Traiter les valeurs manquantes** selon des stratégies configurables.
4. **Calculer des agrégats journaliers** (températures/pressions min, max, moyennes par station).
5. **Détecter les anomalies** climatiques (via Z-score ou IQR).
6. **Charger les résultats** dans une base de données relationnelle SQLite.
7. **Générer des graphiques** de restitution visuelle au format PNG.

L'ensemble de la chaîne est piloté par un fichier de configuration centralisé (`config.yaml`).

---

## 🏗️ Architecture du dépôt

```text
MeteoETL/
├── data/
│   ├── raw/            # Données brutes (ignoré par Git)
│   ├── processed/      # Données transformées (ignoré par Git)
│   └── sample/         # Échantillon de données (< 1 Mo) pour les tests
├── docs/               # Preuves d'historique et rapport final
├── scripts/
│   └── fetch_sample.py # Script de récupération des données d'échantillon
├── src/                # Code source des modules du pipeline
│   ├── csv_ingest.py
│   ├── cleaning.py
│   ├── missing_values.py
│   ├── daily_aggregates.py
│   ├── anomaly_detection.py
│   ├── sqlite_load.py
│   ├── charts.py
│   └── config.py
├── tests/              # Tests unitaires (pytest)
├── .gitignore
├── CHANGELOG.md
├── config.yaml
├── CONTRIBUTING.md
├── README.md
├── requirements.txt
└── VERSION
```

---

## ⚙️ Prérequis et Installation

### Prérequis
- **Python 3.10+** installé sur votre machine.
- **Git** pour le clonage du dépôt.

### Installation
1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/safouatehafsa6/MeteoETL.git
   cd MeteoETL
   ```
   *(Alternative SSH : `git clone git@github.com:safouatehafsa6/MeteoETL.git`)*

2. **Créer et activer un environnement virtuel (recommandé) :**
   ```bash
   python -m venv .venv
   # Sur Linux/macOS :
   source .venv/bin/activate
   # Sur Windows :
   .venv\Scripts\activate
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Configuration et Exécution

### 1. Configuration (`config.yaml` et `src/config.py`)
Les chemins des fichiers, les stratégies de traitement des valeurs manquantes, les seuils de détection d'anomalies (Z-score / IQR) et les paramètres d'exécution sont centralisés dans **`config.yaml`** et chargés via **`src/config.py`**. Pensez à vérifier ou adapter `config.yaml` selon vos besoins avant d'exécuter le pipeline.

### 2. Récupération des données (`scripts/fetch_sample.py`)
Pour préparer l'échantillon de données de test :
```bash
python scripts/fetch_sample.py
```

### 3. Exécution des tests unitaires (`pytest`)
Les tests s'exécutent directement sur l'échantillon de données fourni dans `data/sample/` :
```bash
pytest
```

### Données complètes
Conformément aux bonnes pratiques Git, les jeux de données volumineux (`data/raw/` et `data/processed/`) ne sont pas versionnés.
- Un fichier d'échantillon léger est disponible dans `data/sample/` pour valider le bon fonctionnement du pipeline.
- *[Optionnel : Ajouter ici le lien ou la source du jeu de données complet si applicable].*

---

## 🧩 Fonctionnalités et Auteures (Équipe E3)

Chaque fonctionnalité est développée sur une branche `feature/*` dédiée, accompagnée de ses tests unitaires et relue par un autre membre de l'équipe :

| Fonctionnalité | Branche | Module | Description | Auteure |
| :--- | :--- | :--- | :--- | :--- |
| **Ingestion CSV** | `feature/csv-ingest` | `src/csv_ingest.py` | Chargement des fichiers CSV et contrôle des colonnes attendues | **MASROUR Hafsa** |
| **Nettoyage** | `feature/cleaning` | `src/cleaning.py` | Suppression des doublons, typage et filtrage des valeurs aberrantes | **TAIR Zahra** |
| **Valeurs manquantes** | `feature/missing-values` | `src/missing_values.py` | Imputation par interpolation, moyenne ou suppression | **AOUZAL Salma** |
| **Agrégats journaliers** | `feature/daily-aggregates` | `src/daily_aggregates.py` | Calcul des statistiques (min, max, moyenne) par jour et station | **MBA ZOGHE Rama Fiona** |
| **Détection d'anomalies** | `feature/anomaly-detection` | `src/anomaly_detection.py` | Identification des valeurs inhabituelles (Z-score / IQR) | **CHEMMAOUI Meryem** |
| **Chargement SQLite** | `feature/sqlite-load` | `src/sqlite_load.py` | Sauvegarde des données transformées dans une base SQLite | **SAFOUATE Hafsa** |
| **Visualisation** | `feature/charts` | `src/charts.py` | Génération des graphiques météo (export PNG via `matplotlib`) | **HAMOUCHI Zineb** |
| **Configuration YAML** | `feature/config-yaml` | `src/config.py` | Lecture centralisée des paramètres et seuils via `config.yaml` | **EL HARIRY Soukaina** |

### 🤝 Contribution externe (Anneau inter-équipes)
- **Équipe E2 (`LogAnalytics`)** : *[À compléter lors de la fusion de la PR externe de l'équipe E2]*

---

## 👥 Organisation de l'équipe

- **Release Manager (RM) :** SAFOUATE Hafsa
- **Intégratrice :** HAMOUCHI Zineb
- **Documentaliste :** CHEMMAOUI Meryem

Pour participer au projet ou consulter les règles de contribution (GitFlow, conventions de commits, ordre des relectures), veuillez consulter le fichier [`CONTRIBUTING.md`](CONTRIBUTING.md).