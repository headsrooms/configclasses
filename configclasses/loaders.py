import configparser
import os
from json import loads
from pathlib import Path
from typing import Dict

from configclasses.exceptions import DependencyNotInstalled
from configclasses.helpers import normalize_field_name


def load_env(path):
    try:
        from dotenv import load_dotenv
    except ImportError:
        raise DependencyNotInstalled("You must install 'python-dotenv'")
    load_dotenv(dotenv_path=path)


def load_dict(dict: Dict[str, str]):
    for k, v in dict.items():
        if isinstance(v, Dict):
            inner_dict = {
                f"{k}_{inner_key}": inner_value for inner_key, inner_value in v.items()
            }
            load_dict(inner_dict)
            continue
        os.environ[normalize_field_name(k)] = str(v)


def load_toml(path: Path):
    try:
        from tomlkit import parse
    except ImportError:
        raise DependencyNotInstalled("You must install 'tomlkit'")

    with path.open("r") as config_file:
        cfg = parse(config_file.read())
    load_dict(cfg)


def load_yaml(path: Path):
    try:
        from yaml import full_load
    except ImportError:
        raise DependencyNotInstalled("You must install pyyaml")

    with path.open("r") as config_file:
        cfg = full_load(config_file.read())
    load_dict(cfg)


def load_ini(path: Path):
    cfg = configparser.ConfigParser()
    cfg.read(path)
    load_dict(cfg.__dict__["_sections"])


def load_json(path: Path):
    with path.open("r") as config_file:
        cfg = loads(config_file.read())
    load_dict(cfg)
