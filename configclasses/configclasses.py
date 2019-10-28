import os
from dataclasses import _process_class, fields, is_dataclass
from pathlib import Path
from typing import Dict, Tuple, Any, List, Optional

from configclasses.loaders import file_to_env

supported_extensions = (".env", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".json")


class NonSupportedExtension(Exception):
    pass


class ConfigFilePathDoesNotExist(Exception):
    pass


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
    prefix=None,
):
    """Same behaviour that dataclass with additional classmethods as dataclass intializer: from_environ and from_path
    """

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
    CONVERTER_TYPES = (int, float)

    def from_environ(
        cls, defaults: Dict[str, str] = None, parent_field_name: Optional[str] = None
    ):
        def get_field_value_from_environ(field_name: Any):
            return os.environ.get(str.upper(field_name)) or os.environ.get(
                field_name
            )

        def get_default_value(field_name: Any):
            if defaults:
                return defaults.get(str.upper(field_name)) or defaults.get(
                    field_name
                )

        def fill_init_dict(class_fields: List[Tuple[Any, Any, Any]]):
            init_dict = {}
            for class_field_name, class_field_type, class_field_default in class_fields:
                origin_field_name = (
                    f"{parent_field_name}_{class_field_name}"
                    if parent_field_name
                    else class_field_name
                )
                if is_dataclass(class_field_type):
                    init_dict[class_field_name] = class_field_type.from_environ(
                        defaults, origin_field_name
                    )
                elif field_value := get_field_value_from_environ(
                        origin_field_name
                ) or get_default_value(origin_field_name):
                    if class_field_type in CONVERTER_TYPES:
                        init_dict[class_field_name] = class_field_type(field_value)
                    elif class_field_type == bool:
                        init_dict[class_field_name] = (
                                field_value == "True" or field_value == "true"
                        )
                    else:
                        init_dict[class_field_name] = field_value
                else:
                    init_dict[class_field_name] = class_field_default

            return init_dict

        fields_tuple = [
            (field.name, field.type, field.default) for field in fields(cls)
        ]
        init_dict = fill_init_dict(fields_tuple)
        return cls(**init_dict)

    def from_path(cls, config_path: str, defaults: Dict[str, str] = None):
        def path_to_env(path: Path):
            """Given a path it loads into os.environ all config files found in this path.
            """
            if not path.exists():
                raise ConfigFilePathDoesNotExist()
            if path.is_file():
                extension = path.suffix
                if extension in supported_extensions:
                    file_to_env(extension, path)
                else:
                    raise NonSupportedExtension()
            else:
                for x in path.iterdir():
                    path_to_env(x)

        path_to_env(Path(config_path))
        return cls.from_environ(defaults)

    cls.from_environ = classmethod(from_environ)
    cls.from_path = classmethod(from_path)

    return cls
