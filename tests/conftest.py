import pytest

from configclasses.configclasses import configclass


@pytest.fixture
def a_configclass():
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
