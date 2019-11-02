# configclasses

![PyPI](https://img.shields.io/pypi/v/12factor-configclasses)
[![codecov](https://codecov.io/gh/kingoodie/configclasses/branch/master/graph/badge.svg)](https://codecov.io/gh/kingoodie/configclasses)
<a href="https://codeclimate.com/github/kingoodie/configclasses/maintainability"><img src="https://api.codeclimate.com/v1/badges/9094f65f5caef64fb993/maintainability" /></a>


Like dataclases but for config.


```python
>>> import os
... 
... from configclasses import configclass
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
... @configclass
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

## Requirements

Python 3.8+


## Installation

    pip install 12factor-configclasses
    
## Supported formats

- .env ->   ```pip install 12factor-configclasses[dotenv]```
- .yaml ->   ```pip install 12factor-configclasses[yaml]```
- .toml ->   ```pip install 12factor-configclasses[toml]```
- .ini
- .json

Install all dependencies with:

    pip install 12factor-configclasses[full]
    
## Example

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
    
    
    os.environ["APP_DEFAULT_PRICE"] = "22"
    cfg = AppConfig.from_environ(
        {"app_db_driver": "postgres", "APP_DB_USER": "matt"}
    )  # it takes values from os.environ by default, if some key is not provided it fills with values in dict
    print(cfg)
    print(cfg.db)
    
    cfg_2 = AppConfig.from_path(
        config_path="tests/example/conf/config.toml",
        defaults={"APP_DB_HOST": "localhost", "app_db_driver": "redis", "default_price": "ignored"},
    )
    print(cfg_2)

    