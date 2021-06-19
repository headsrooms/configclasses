import pytest

from configclasses import configclass


@pytest.fixture
def a_configclass():
    @configclass
    class DB:
        driver: str
        host: str
        port: int
        user: str
        password: str

    @configclass()
    class AppConfig:
        db: DB
        default_price: float
        only_pub: bool = False

    return AppConfig


@pytest.fixture
def a_configclass_with_prefix():
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

    return AppConfig


@pytest.fixture
def another_configclass():
    @configclass
    class DB:
        user: str
        password: str
        url: str

    @configclass
    class AppConfig:
        host: str
        port: int
        db: DB
        generate_schemas: bool
        debug: bool
        https_only: bool
        gzip: bool
        sentry: bool

    return AppConfig