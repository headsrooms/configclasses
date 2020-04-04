import os
from pathlib import Path

import pytest

from configclasses import configclass
from configclasses.exceptions import ConfigFilePathDoesNotExist


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


def test_path_to_env_if_path_is_a_json_string(a_configclass):
    test_json = """{"OUTER_INT": 1,"section": {
                "INNER_FLOAT": 3.4,
                "inner_bool": false,
                "INNER_STRING": "hola"}}"""
    a_configclass.from_string(test_json, ".json")
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


def test_readme_exampe_from_string():
    @configclass
    class DB:
        user: str
        password: str
        url: str

    @configclass
    class AppConfig:
        host: str
        port: int
        db: DB
        generate_schemas: bool
        debug: bool
        https_only: bool
        gzip: bool
        sentry: bool

    test_env = """
    HOST=0.0.0.0
    PORT=8000
    DB_URL=sqlite://:memory:
    GENERATE_SCHEMAS=True
    DEBUG=True
    HTTPS_ONLY=False
    GZIP=True
    SENTRY=False"""
    app_config = AppConfig.from_string(test_env, ".env")
    assert app_config.port == 8000
    assert app_config.db.url == "sqlite://:memory:"
