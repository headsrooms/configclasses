import os
from pathlib import Path

from configclasses.configclasses import file_to_env
from configclasses.helpers import normalize_field_name
from configclasses.loaders import (
    load_dict,
    load_toml,
    load_yaml,
    load_ini,
    load_json,
    load_env,
)


def test_normalize_field_name():
    assert normalize_field_name("A_THING") == "a_thing"


def test_file_to_env_dotenv():
    file_to_env(".env", Path("tests/test_files/.env"))
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


def test_load_toml_with_string():
    test_toml = '''OUTER_INT = 1
                [section_1]
                INNER_FLOAT = 3.4
                
                [other_section]
                inner_bool = false
                
                INNER_STRING = "hola"'''
    load_toml(string=test_toml)
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_1_inner_float"] == "3.4"
    assert os.environ["other_section_inner_bool"] == "False"
    assert os.environ["other_section_inner_string"] == "hola"


def test_load_yaml_with_string():
    test_yaml = """
                OUTER_INT: 1
                INNER_FLOAT: 3.4
                inner_bool: false
                INNER_STRING: hola"""
    load_yaml(string=test_yaml)
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_1_inner_float"] == "3.4"
    assert os.environ["other_section_inner_bool"] == "False"
    assert os.environ["other_section_inner_string"] == "hola"


def test_load_ini_with_string():
    test_ini = """[section]
                OUTER_INT = 1
                INNER_FLOAT = 3.4
                inner_bool = false
                INNER_STRING = hola"""
    load_ini(string=test_ini)
    assert os.environ["section_outer_int"] == "1"
    assert os.environ["section_inner_float"] == "3.4"
    assert os.environ["section_inner_bool"] == "false"
    assert os.environ["section_inner_string"] == "hola"


def test_load_json_with_string():
    test_json = """{"OUTER_INT": 1,"section": {
                "INNER_FLOAT": 3.4,
                "inner_bool": false,
                "INNER_STRING": "hola"}}"""
    load_json(string=test_json)
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_inner_float"] == "3.4"
    assert os.environ["section_inner_bool"] == "False"
    assert os.environ["section_inner_string"] == "hola"


def test_file_to_env_dotenv_with_string():
    env_string = """OUTER_INT = 1
    INNER_FLOAT = 3.4
    inner_bool = false
    INNER_STRING = hola"""
    load_env(string=env_string)
    assert os.environ["outer_int"] == "1"
    assert os.environ["section_1_inner_float"] == "3.4"
    assert os.environ["other_section_inner_bool"] == "False"
    assert os.environ["other_section_inner_string"] == "hola"
