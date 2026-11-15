"""Module de lecture de la configuration YAML du pipeline MeteoETL."""

from pathlib import Path
import yaml


def load_config(path: str) -> dict:
    """
    Charge un fichier de configuration YAML et retourne un dictionnaire.

    Args:
        path (str): Chemin vers le fichier YAML.

    Returns:
        dict: Dictionnaire des paramètres.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        ValueError: Si le fichier est vide ou mal formé.
    """
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if config is None:
        raise ValueError(f"Le fichier de configuration est vide : {path}")

    if not isinstance(config, dict):
        raise ValueError(
            f"Le fichier de configuration doit contenir un dictionnaire : {path}"
        )

    return config
