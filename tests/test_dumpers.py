from pathlib import Path

from configclasses import configclass
from configclasses.dumpers import dump_env, dump_json


def test_dump_env(another_configclass):

    test_env = """
    HOST=0.0.0.0
    PORT=8000
    DB_URL=sqlite://:memory:
    GENERATE_SCHEMAS=True
    DEBUG=True
    HTTPS_ONLY=False
    GZIP=True
    SENTRY=False"""

    app_config = another_configclass.from_string(test_env, ".env")
    test_file = Path("test.env")
    dump_env(app_config, test_file)
    app_config_copy = another_configclass.from_path(test_file)
    assert app_config == app_config_copy

    test_file.unlink()


def test_dump_json(another_configclass):
    test_json = """{
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "DB": {"URL": "sqlite://:memory:"},
        "GENERATE_SCHEMAS": true,
        "DEBUG": true,
        "HTTPS_ONLY": false,
        "GZIP": true,
        "SENTRY": false}"""

    app_config = another_configclass.from_string(test_json, ".json")
    test_file = Path("test.json")
    dump_json(app_config, test_file)
    app_config_copy = another_configclass.from_path(test_file)
    assert app_config == app_config_copy

    test_file.unlink()
