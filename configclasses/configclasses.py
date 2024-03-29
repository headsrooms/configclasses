import inspect
from dataclasses import _process_class, fields
from os import PathLike
from pathlib import Path
from typing import Dict, Optional

from configclasses.dumpers import dump_env, dump_ini, dump_json, dump_toml, dump_yaml
from configclasses.exceptions import ConfigFilePathDoesNotExist, NonSupportedExtension
from configclasses.helpers import fill_init_dict, supported_extensions
from configclasses.loaders import load_env, load_ini, load_json, load_toml, load_yaml


def configclass(
    cls=None,
    /,
    *,
    prefix: Optional[str] = None,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    match_args=True,
    kw_only=False,
    slots=False,
    weakref_slot=False,
):
    """Same behaviour that dataclass with additional classmethods as dataclass initializers:
    from_environ and from_path"""

    def wrap(cls):
        signature = inspect.signature(_process_class)
        kwargs = {}
        if "match_args" in signature.parameters:
            kwargs["match_args"] = match_args
        if "kw_only" in signature.parameters:
            kwargs["kw_only"] = kw_only
        if "slots" in signature.parameters:
            kwargs["slots"] = slots
        if "weakref_slot" in signature.parameters:
            kwargs["weakref_slot"] = weakref_slot

        return _post_process_class(
            _process_class(cls, init, repr, eq, order, unsafe_hash, frozen, **kwargs),
            prefix,
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

    def from_string(cls, string: str, extension: str, defaults: Dict[str, str] = None):
        load_file(string=string, extension=extension)
        return cls.from_environ(defaults)

    the_class.from_environ = classmethod(from_environ)
    the_class.from_path = classmethod(from_path)
    the_class.from_string = classmethod(from_string)

    return the_class


def path_to_env(path: Path):
    """Given a path it loads into os.environ all config files found in this path."""
    if not path.exists():
        raise ConfigFilePathDoesNotExist(
            f"Config file path '{str(path)}' does not exist"
        )
    if path.is_file():
        load_file(path)
    else:
        load_path(path)


def file_to_env(
    extension: str, path: Optional[Path] = None, string: Optional[str] = None
):
    if extension == ".env":
        load_env(path, string)
    elif extension == ".toml":
        load_toml(path, string)
    elif extension in (".yaml", ".yml"):
        load_yaml(path, string)
    elif extension in (".ini", ".cfg"):
        load_ini(path, string)
    elif extension == ".json":
        load_json(path, string)


def load_path(path: Path):
    for x in path.iterdir():
        path_to_env(x)


def load_file(
    path: Optional[Path] = None,
    string: Optional[str] = None,
    extension: Optional[str] = None,
):
    extension = path.suffix or path.name if path else extension
    if extension in supported_extensions:
        file_to_env(extension, path, string)
    else:
        raise NonSupportedExtension(f"Extension '{extension}' not supported")


def dump(
    obj,
    path: Optional[PathLike] = None,
    extension: Optional[str] = None,
):
    path = Path(path) if path else None
    extension = path.suffix or path.name if path else extension
    if extension in supported_extensions:
        if extension == ".env":
            dump_env(obj, path)
        elif extension == ".toml":
            dump_toml(obj, path)
        elif extension in (".yaml", ".yml"):
            dump_yaml(obj, path)
        elif extension in (".ini", ".cfg"):
            dump_ini(obj, path)
        elif extension == ".json":
            dump_json(obj, path)
    else:
        raise NonSupportedExtension(f"Extension '{extension}' not supported")
