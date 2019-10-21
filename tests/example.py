import os

from configclasses import configclass


@configclass
class DB:
    driver: str
    host: str
    port: int
    user: str
    password: str


@configclass(prefix="APP")
class AppConfig:
    db: DB
    default_price: float
    only_pub: bool = False


os.environ["default_price"] = "22"
cfg = AppConfig.from_environ(
    {"db": "postgres", "APP_DB_USER": "matt"}
)  # it takes values from os.environ by default, if some key is not provided it fills with values in dict
print(cfg)

cfg_2 = AppConfig.from_file(config_path="conf/config.toml",
                            defaults={"APP_DB_HOST": "localhost", "db": "redis", "default_price": "ignored"})
print(cfg_2)
