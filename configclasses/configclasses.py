from dataclasses import _process_class, fields
from pathlib import Path
from typing import Dict, Optional

from configclasses.exceptions import ConfigFilePathDoesNotExist, NonSupportedExtension
from configclasses.helpers import fill_init_dict, supported_extensions
from configclasses.loaders import (
    load_env,
    load_toml,
    load_yaml,
    load_ini,
    load_json,
)


def configclass(
    cls=None, /, *, prefix: Optional[str] = None, **dataclass_parameters,
):
    """Same behaviour that dataclass with additional classmethods as dataclass intializers: from_environ and from_path
    """

    init = dataclass_parameters.get("init", True)
    repr = dataclass_parameters.get("repr", True)
    eq = dataclass_parameters.get("eq", True)
    order = dataclass_parameters.get("order", False)
    unsafe_hash = dataclass_parameters.get("unsafe_hash", False)
    frozen = dataclass_parameters.get("frozen", True)

    def wrap(cls):
        return _post_process_class(
            _process_class(cls, init, repr, eq, order, unsafe_hash, frozen), prefix
        )

    # See if we're being called as @configclass or @configclass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dataclass without parens.
    return wrap(cls)


def _post_process_class(the_class, the_prefix: Optional[str]):
    def from_environ(
        cls, defaults: Dict[str, str] = None, parent_field_name: Optional[str] = None
    ):
        fields_tuple = [
            (field.name, field.type, field.default) for field in fields(cls)
        ]
        init_dict = fill_init_dict(
            fields_tuple, defaults, parent_field_name, the_prefix
        )
        return cls(**init_dict)

    def from_path(cls, config_path: str, defaults: Dict[str, str] = None):
        path_to_env(Path(config_path))
        return cls.from_environ(defaults)

    the_class.from_environ = classmethod(from_environ)
    the_class.from_path = classmethod(from_path)

    return the_class


def path_to_env(path: Path):
    """Given a path it loads into os.environ all config files found in this path.
    """
    if not path.exists():
        raise ConfigFilePathDoesNotExist(
            f"Config file path '{str(path)}' does not exist"
        )
    if path.is_file():
        load_file(path)
    else:
        load_path(path)


def file_to_env(extension: str, path: Path):
    if extension == ".env":
        load_env(path)
    elif extension == ".toml":
        load_toml(path)
    elif extension == ".yaml" or extension == ".yml":
        load_yaml(path)
    elif extension == ".ini" or extension == ".cfg":
        load_ini(path)
    elif extension == ".json":
        load_json(path)


def load_path(path):
    for x in path.iterdir():
        path_to_env(x)


def load_file(path):
    extension = path.suffix or path.name
    if extension in supported_extensions:
        file_to_env(extension, path)
    else:
        raise NonSupportedExtension(f"Extension '{extension}' not supported")
