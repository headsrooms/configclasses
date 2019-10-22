import os
from abc import abstractmethod
from dataclasses import _process_class, fields
from pathlib import Path
from typing import Dict, runtime_checkable, Protocol, Union, Tuple, Any, List

from dotenv import load_dotenv
from tomlkit import parse

supported_extensions = (".env", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".json")


class NonSupportedExtension(Exception):
    pass


class ConfigFilePathDoesNotExist(Exception):
    pass


@runtime_checkable
class SupportsStr(Protocol):
    """An ABC with one abstract method __str__."""
    __slots__ = ()

    @abstractmethod
    def __str__(self) -> str:
        pass


def normalize_field_name(field_name: Union[SupportsStr, str]):
    return str.lower(str(field_name))


def load_dict(dict: Dict[str, str]):
    for k, v in dict.items():
        os.environ[normalize_field_name(k)] = str(v)


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


def extension_to_env(extension: str, path: Union[Path, os.PathLike]):
    if extension == ".env":
        load_dotenv(dotenv_path=path)
    elif extension == ".toml":
        load_toml(path)
    elif extension == ".yaml" or extension == ".yml":
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

    def initialize_init_dict(fields: List[Tuple[Any, Any, Any]], defaults: Dict[str, str]):
        def get_field_value(field_name: Any):
            return os.environ.get(str.upper(field_name)) or os.environ.get(field_name) or defaults.get(field_name)

        init_dict = dict()
        for field_name, field_type, field_default in fields:
            if field_value := get_field_value(field_name):
                converter = field_type if field_type in CONVERTER_TYPES else None
                init_dict[field_name] = (
                    converter(field_value) if converter else field_value
                )
            else:
                init_dict[field_name] = field_default
        return init_dict


    @classmethod
    def from_environ(cls, defaults: Dict[str, str]):
        fields_tuple = [(field.name, field.type, field.default) for field in fields(cls)]
        init_dict = initialize_init_dict(fields_tuple, defaults)

        return cls(**init_dict)

    @classmethod
    def from_file(cls, config_path: str, defaults: Dict[str, str]):
        path_to_env(Path(config_path))
        return cls.from_environ(defaults)

    cls.from_environ = from_environ
    cls.from_file = from_file

    return cls
