import os
from pathlib import Path

from configclasses.loaders import (
    normalize_field_name,
    load_dict,
    load_toml,
    load_yaml,
    load_ini,
    load_json,
    file_to_env,
)


def test_normalize_field_name():
    assert normalize_field_name("A_THING") == "a_thing"


def test_file_to_env_dotenv():
    file_to_env(".env", Path("tests/test_files/test.env"))
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_1_inner_float"] == "3.4"
    assert os.environ["other_section_inner_bool"] == "False"
    assert os.environ["other_section_inner_string"] == "hola"


def test_load_dict():
    env_dict = {"A_FLOAT": 3.4, "a_bool": True, "an_int": 44, "A_STRING": "k3k3"}
    load_dict(env_dict)

    assert os.environ["a_float"] == "3.4"
    assert os.environ["a_bool"] == "True"
    assert os.environ["an_int"] == "44"
    assert os.environ["a_string"] == "k3k3"


def test_load_toml():
    load_toml(Path("tests/test_files/test.toml"))
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_1_inner_float"] == "3.4"
    assert os.environ["other_section_inner_bool"] == "False"
    assert os.environ["other_section_inner_string"] == "hola"


def test_load_yaml():
    load_yaml(Path("tests/test_files/test.yaml"))
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_1_inner_float"] == "3.4"
    assert os.environ["other_section_inner_bool"] == "False"
    assert os.environ["other_section_inner_string"] == "hola"


def test_load_ini():
    load_ini(Path("tests/test_files/test.ini"))
    assert os.environ["section_outer_int"] == "1"
    assert os.environ["section_inner_float"] == "3.4"
    assert os.environ["section_inner_bool"] == "false"
    assert os.environ["section_inner_string"] == "hola"


def test_load_json():
    load_json(Path("tests/test_files/test.json"))
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_inner_float"] == "3.4"
    assert os.environ["section_inner_bool"] == "False"
    assert os.environ["section_inner_string"] == "hola"
