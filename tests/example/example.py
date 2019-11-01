import os

from configclasses.configclasses import configclass


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


os.environ["APP_DEFAULT_PRICE"] = "22"
cfg = AppConfig.from_environ(
    {"app_db_driver": "postgres", "APP_DB_USER": "matt"}
)  # it takes values from os.environ by default, if some key is not provided it fills with values in dict
print(cfg)
print(cfg.db)

cfg_2 = AppConfig.from_path(
    config_path="tests/example/conf/config.toml",
    defaults={
        "APP_DB_HOST": "localhost",
        "app_db_driver": "redis",
        "default_price": "ignored",
    },
)
print(cfg_2)
