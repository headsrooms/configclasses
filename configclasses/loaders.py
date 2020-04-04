import configparser
import os
from io import StringIO
from json import loads
from pathlib import Path
from typing import Dict, Optional

from configclasses.exceptions import DependencyNotInstalled
from configclasses.helpers import normalize_field_name


def load_env(path: Optional[Path] = None, string: Optional[str] = None):
    try:
        from dotenv import load_dotenv
    except ImportError:
        raise DependencyNotInstalled("You must install 'python-dotenv'")
    if path:
        load_dotenv(dotenv_path=path)
    else:
        load_dotenv(stream=StringIO(string))


def load_dict(dict: Dict[str, str]):
    for k, v in dict.items():
        if isinstance(v, Dict):
            inner_dict = {
                f"{k}_{inner_key}": inner_value for inner_key, inner_value in v.items()
            }
            load_dict(inner_dict)
            continue
        os.environ[normalize_field_name(k)] = str(v)


def load_toml(path: Optional[Path] = None, string: Optional[str] = None):
    try:
        from tomlkit import parse
    except ImportError:
        raise DependencyNotInstalled("You must install 'tomlkit'")

    if path:
        with path.open("r") as config_file:
            cfg = parse(config_file.read())
    else:
        cfg = parse(string)
    load_dict(cfg)


def load_yaml(path: Optional[Path] = None, string: Optional[str] = None):
    try:
        from yaml import full_load
    except ImportError:
        raise DependencyNotInstalled("You must install pyyaml")

    if path:
        with path.open("r") as config_file:
            cfg = full_load(config_file.read())
    else:
        cfg = full_load(string)
    load_dict(cfg)


def load_ini(path: Optional[Path] = None, string: Optional[str] = None):
    cfg = configparser.ConfigParser()
    cfg.read(path) if path else cfg.read_string(string)
    load_dict(cfg.__dict__["_sections"])


def load_json(path: Optional[Path] = None, string: Optional[str] = None):
    if path:
        with path.open("r") as config_file:
            cfg = loads(config_file.read())
    else:
        cfg = loads(string)
    load_dict(cfg)
