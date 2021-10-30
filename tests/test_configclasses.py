import os
from pathlib import Path

import pytest

from configclasses import configclass
from configclasses.exceptions import ConfigFilePathDoesNotExist


def test_path_to_env_inexistent_path(a_configclass):
    with pytest.raises(ConfigFilePathDoesNotExist):
        a_configclass.from_path(Path("nothing"))


def test_path_to_env_if_path_is_a_toml_file(a_configclass):
    a_configclass.from_path(Path("tests/test_files/configclass.toml"))
    assert os.environ["db_driver"] == "postgres"


def test_path_to_env_if_path_is_a_yaml_file(a_configclass):
    a_configclass.from_path(Path("tests/test_files/configclass.yaml"))
    assert os.environ["db_driver"] == "mongodb"


def test_path_to_env_if_path_is_a_ini_file(a_configclass):
    a_configclass.from_path(Path("tests/test_files/configclass.ini"))
    assert os.environ["db_user"] == "pain"


def test_path_to_env_if_path_is_a_json_file(a_configclass):
    a_configclass.from_path(Path("tests/test_files/configclass.json"))
    assert os.environ["db_port"] == "321"


def test_path_to_env_if_path_is_a_json_string(a_configclass):
    test_json = """{
      "default_price": 1,
      "only_pub": false,
      "db": {
        "driver": "bq",
        "host": "localhost",
        "port": 321,
        "user": "lonershy",
        "password": "pass"
      }
    }"""
    a_configclass.from_string(test_json, ".json")
    assert os.environ["db_password"] == "pass"


def test_path_to_env_if_path_is_a_dir(a_configclass):
    a_configclass.from_path(Path("tests/test_files/configclass_path/"))
    assert os.environ["DB_HOST"] == "192.168.1.11"


def test_from_environ(a_configclass):
    os.environ["DEFAULT_PRICE"] = "22"
    os.environ["ONLY_PUB"] = "True"
    os.environ.pop("DB_USER")
    os.environ.pop("db_user")
    cfg = a_configclass.from_environ({"db_driver": "mssql", "db_user": "matt"})
    assert cfg.default_price == 22
    assert cfg.only_pub is True
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


def test_readme_example_from_string():
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
