import os
from dataclasses import is_dataclass
from typing import Any, Dict, List, Tuple, Optional

supported_extensions = (".env", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".json")
converter_types = (int, float)


def get_field_value_from_environ(field_name: Any):
    return os.environ.get(str.upper(field_name)) or os.environ.get(field_name)


def get_default_value(field_name: Any, defaults: Dict[str, str]) -> Optional[str]:
    if defaults:
        return defaults.get(str.upper(field_name)) or defaults.get(field_name)


def fill_init_dict(
    class_fields: List[Tuple[Any, Any, Any]], defaults, parent_field_name, prefix
):
    init_dict = {}
    for class_field_name, class_field_type, class_field_default in class_fields:
        origin_field_name = get_origin_field_name(
            class_field_name, parent_field_name, prefix
        )

        if is_dataclass(class_field_type):
            init_dict[class_field_name] = class_field_type.from_environ(
                defaults, origin_field_name
            )
        elif field_value := get_field_value_from_environ(
            origin_field_name
        ) or get_default_value(origin_field_name, defaults):
            fill_with_environ_or_provided_defaults(
                class_field_name, class_field_type, field_value, init_dict
            )
        else:
            init_dict[class_field_name] = class_field_default

    return init_dict


def fill_with_environ_or_provided_defaults(
    class_field_name, class_field_type, field_value, init_dict
):
    if class_field_type in converter_types:
        init_dict[class_field_name] = class_field_type(field_value)
    elif class_field_type == bool:
        init_dict[class_field_name] = field_value in ("True", "true")
    else:
        init_dict[class_field_name] = field_value


def get_origin_field_name(class_field_name, parent_field_name, prefix):
    if not prefix and not parent_field_name:
        origin_field_name = class_field_name
    elif parent_field_name:
        origin_field_name = f"{parent_field_name}_{class_field_name}"
    elif prefix:
        origin_field_name = f"{prefix}_{class_field_name}"
    else:
        origin_field_name = f"{prefix}_{parent_field_name}_{class_field_name}"
    return origin_field_name


def normalize_field_name(field_name: str):
    return str.lower(str(field_name))
