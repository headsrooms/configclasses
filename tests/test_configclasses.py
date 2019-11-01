import os
from pathlib import Path

import pytest

from configclasses.configclasses import ConfigFilePathDoesNotExist


def test_path_to_env_inexistent_path(a_configclass):
    with pytest.raises(ConfigFilePathDoesNotExist):
        a_configclass.from_path(Path("nothing"))


def test_path_to_env_if_path_is_a_toml_file(a_configclass):
    a_configclass.from_path(Path("tests/test_files/test.toml"))
    assert os.environ["section_1_inner_float"] == "3.4"


def test_path_to_env_if_path_is_a_yaml_file(a_configclass):
    a_configclass.from_path(Path("tests/test_files/test.yaml"))
    assert os.environ["inner_string"] == "hola"


def test_path_to_env_if_path_is_a_ini_file(a_configclass):
    a_configclass.from_path(Path("tests/test_files/test.ini"))
    assert os.environ["section_inner_bool"] == "false"


def test_path_to_env_if_path_is_a_json_file(a_configclass):
    a_configclass.from_path(Path("tests/test_files/test.json"))
    assert os.environ["outer_int"] == "1"


def test_path_to_env_if_path_is_a_dir(a_configclass):
    a_configclass.from_path(Path("tests/test_files/"))
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_inner_bool"] == "False"
    assert os.environ["inner_string"] == "hola"
    assert os.environ["section_1_inner_float"] == "3.4"


def test_from_environ(a_configclass):
    os.environ["DEFAULT_PRICE"] = "22"
    os.environ["ONLY_PUB"] = "True"
    cfg = a_configclass.from_environ({"db_driver": "postgres", "DB_USER": "matt"})
    assert cfg.default_price == 22
    assert cfg.only_pub == True
    assert cfg.db.user == "matt"


def test_prefix_parameter_works(a_configclass_with_prefix):
    os.environ["APP_DB_HOST"] = "localhost"
    os.environ["APP_DB_PORT"] = "8432"
    cfg = a_configclass_with_prefix.from_environ(
        {"app_db_driver": "postgres", "APP_DB_USER": "katie"}
    )
    assert cfg.db.port == 8432
    assert cfg.db.host == "localhost"
    assert cfg.db.user == "katie"
