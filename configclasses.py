import os
from dataclasses import _process_class, fields
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

from tomlkit import parse

supported_extensions = (".env", ".toml", ".yaml", ".ini", ".cfg", ".json")


class NonSupportedExtension(Exception):
    pass


class ConfigFilePathDoesNotExist(Exception):
    pass


def load_dict(dict: Dict[str, str]):
    for k, v in dict.items():
        os.environ[str(k)] = str(v)


def load_toml(path: Path):
    with path.open("r") as config_file:
        cfg = parse(config_file.read())
    load_dict(cfg)


def load_yaml(path: Path):
    pass


def load_ini(path: Path):
    pass


def load_cfg(path: Path):
    pass


def load_json(path: Path):
    pass


def extension_to_env(extension: str, path: Path):
    if extension == ".env":
        load_dotenv(dotenv_path=path)
    elif extension == ".toml":
        load_toml(path)
    elif extension == ".yaml":
        load_yaml(path)
    elif extension == ".ini":
        load_ini(path)
    elif extension == ".cfg":
        load_cfg(path)
    elif extension == ".json":
        load_json(path)


def path_to_env(path: Path):
    if not path.exists():
        raise ConfigFilePathDoesNotExist()
    if path.is_file():
        extension = path.suffix
        if extension in supported_extensions:
            extension_to_env(extension, path)
        else:
            raise NonSupportedExtension()
    else:
        for x in path.iterdir():
            path_to_env(x)


def configclass(
    cls=None,
    /,
    *,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    prefix=None
):
    def wrap(cls):
        return _post_process_class(
            _process_class(cls, init, repr, eq, order, unsafe_hash, frozen)
        )

    # See if we're being called as @configclass or @configclass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dataclass without parens.
    return wrap(cls)


def _post_process_class(cls):
    CONVERTER_TYPES = (int, float, bool)

    @classmethod
    def from_environ(cls, defaults: Dict[str, str]):
        init_dict = dict()
        for field in fields(cls):
            field_name = field.name

            if field_value := os.environ.get(field_name, defaults.get(field_name)):
                converter = field.type if field.type in CONVERTER_TYPES else None
                init_dict[field_name] = (
                    converter(field_value) if converter else field_value
                )
            else:
                init_dict[field_name] = field.default

        return cls(**init_dict)

    @classmethod
    def from_file(cls, config_path: str, defaults: Dict[str, str]):
        path_to_env(Path(config_path))
        return cls.from_environ(defaults)

    cls.from_environ = from_environ
    cls.from_file = from_file

    return cls
