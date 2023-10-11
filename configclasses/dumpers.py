import json
from dataclasses import _MISSING_TYPE, asdict
from os import PathLike


def dump_env_key(key, value):
    try:
        lines = [
            f"{dump_env_key(key + '_' + sub_key, sub_value)}"
            for sub_key, sub_value in value.__dict__.items()
        ]
        lines = [line for line in lines if line]
        return "\n".join(lines)
    except AttributeError:
        return f"{key}={value}\n"


def dump_env(obj, path: PathLike):
    lines = [f"{dump_env_key(key, value)}" for key, value in obj.__dict__.items()]
    with open(path, "w") as file:
        file.writelines(lines)


def dump_toml(obj, path):
    raise NotImplementedError


def dump_yaml(obj, path):
    raise NotImplementedError


def dump_ini(obj, path):
    raise NotImplementedError


def dump_json_key(value):
    try:
        return {
            key: sub_value
            for key, sub_value in asdict(value).items()
            if not isinstance(sub_value, _MISSING_TYPE)
        }
    except TypeError:
        return value


def dump_json(obj, path: PathLike):
    output = {key: dump_json_key(value) for key, value in obj.__dict__.items()}

    with open(path, "w") as file:
        json.dump(output, file)
