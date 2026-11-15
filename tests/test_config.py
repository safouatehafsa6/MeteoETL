import pytest
from src.config import load_config


def test_load_config_returns_dict(tmp_path):
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(
        "paths:\n  raw_data: data/raw/meteo.csv\n"
        "thresholds:\n  anomaly_zscore: 3.0\n",
        encoding="utf-8",
    )

    result = load_config(str(config_file))

    assert isinstance(result, dict)
    assert result["paths"]["raw_data"] == "data/raw/meteo.csv"
    assert result["thresholds"]["anomaly_zscore"] == 3.0


def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("chemin/inexistant.yaml")


def test_load_config_empty_file(tmp_path):
    empty_file = tmp_path / "empty.yaml"
    empty_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        load_config(str(empty_file))

def test_load_config_malformed_yaml(tmp_path):
    malformed_file = tmp_path / "malformed.yaml"
    malformed_file.write_text("paths:\n  raw_data: [unclosed\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_config(str(malformed_file))
