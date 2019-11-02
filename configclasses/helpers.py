import os
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

from configclasses.loaders import file_to_env


supported_extensions = (".env", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".json")
converter_types = (int, float)


class NonSupportedExtension(Exception):
    pass


class ConfigFilePathDoesNotExist(Exception):
    pass


def get_field_value_from_environ(field_name: Any):
    return os.environ.get(str.upper(field_name)) or os.environ.get(field_name)


def get_default_value(field_name: Any, defaults: Dict[str, str]):
    if defaults:
        return defaults.get(str.upper(field_name)) or defaults.get(field_name)


def fill_init_dict(
    class_fields: List[Tuple[Any, Any, Any]], defaults, parent_field_name, prefix
):
    init_dict = {}
    for class_field_name, class_field_type, class_field_default in class_fields:
        if not prefix and not parent_field_name:
            origin_field_name = class_field_name
        elif parent_field_name:
            origin_field_name = f"{parent_field_name}_{class_field_name}"
        elif prefix:
            origin_field_name = f"{prefix}_{class_field_name}"
        else:
            origin_field_name = f"{prefix}_{parent_field_name}_{class_field_name}"

        if is_dataclass(class_field_type):
            init_dict[class_field_name] = class_field_type.from_environ(
                defaults, origin_field_name
            )
        elif field_value := get_field_value_from_environ(
            origin_field_name
        ) or get_default_value(origin_field_name, defaults):
            if class_field_type in converter_types:
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


def path_to_env(path: Path):
    """Given a path it loads into os.environ all config files found in this path.
    """
    if not path.exists():
        raise ConfigFilePathDoesNotExist(f"Config file path '{str(path)}' does not exist")
    if path.is_file():
        extension = path.suffix
        if extension in supported_extensions:
            file_to_env(extension, path)
        else:
            raise NonSupportedExtension(f"Extension '{extension}' not supported")
    else:
        for x in path.iterdir():
            path_to_env(x)
