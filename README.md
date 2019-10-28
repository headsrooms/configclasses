# configclasses

![PyPI](https://img.shields.io/pypi/v/12factor-configclasses)
[![codecov](https://codecov.io/gh/kingoodie/configclasses/branch/master/graph/badge.svg)](https://codecov.io/gh/kingoodie/configclasses)



Like dataclases but for config.


```python
>>> import os
... 
... from configclasses.configclasses import configclass
... 
... 
... @configclass
... class DB:
...     driver: str
...     host: str
...     port: int
...     user: str
...     password: str
... 
... 
... @configclass(prefix="APP")
... class AppConfig:
...     db: DB
...     default_price: float
...     only_pub: bool = False
...     
>>> os.environ["DEFAULT_PRICE"] = "22"
... cfg = AppConfig.from_environ(
...     {"db_driver": "postgres", "DB_USER": "matt"}
... )  # it takes values from os.environ by default, if some key is not provided it fills with values in dict
... print(cfg)
... print(cfg.db)
AppConfig(db=DB(driver='postgres', host=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>, port=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>, user='matt', password=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>), default_price=22.0, only_pub=False)
DB(driver='postgres', host=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>, port=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>, user='matt', password=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>)
>>> cfg_2 = AppConfig.from_path(
...     config_path="tests/example/conf/config.toml",
...     defaults={"DB_HOST": "localhost", "db_driver": "redis", "default_price": "ignored"},
... )
... print(cfg_2)
... 
AppConfig(db=DB(driver='redis', host='localhost', port=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>, user=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>, password=<dataclasses._MISSING_TYPE object at 0x000001E6BD1F9640>), default_price=52.1, only_pub=True)

```