# configclasses

![PyPI](https://img.shields.io/pypi/v/12factor-configclasses)
[![codecov](https://codecov.io/gh/headsrooms/configclasses/branch/master/graph/badge.svg?token=U0bxsmAUoe)](https://codecov.io/gh/headsrooms/configclasses)
<a href="https://codeclimate.com/github/kingoodie/configclasses/maintainability"><img src="https://api.codeclimate.com/v1/badges/9094f65f5caef64fb993/maintainability" /></a>


Like dataclasses but for config.

Specify your config with a class and load it with your env vars or env files.


```python
import httpx
from configclasses import configclass


class UserAPIClient(httpx.AsyncClient):
    def __init__(self, config: ClientConfig, *args, **kwargs):
        self.config = config
        super().__init__(*args, **kwargs)

    async def get_users(self, headers: Optional[Headers] = None) -> Dict[str, Any]:
        response = await self.get(f"{self.path}/users", auth=headers)
        response.raise_for_status()
        return response.json()
    
@configclass
class ClientConfig:
    host: str
    port: int

config = ClientConfig.from_path(".env")
async with UserAPIClient(config) as client:
    users = await client.get_users(auth_headers)
```

## Features

- Fill your configclasses with existent env vars.
- Define default values in case these variables have no value at all.
- Load your config files in env vars following [12factor apps](https://12factor.net) recommendations.
- Support for _.env_, _yaml_, _toml_, _ini_ and _json_.
- Convert your env vars with specified type in configclass: `int`, `float`, `str` or `bool`.
- Use nested configclasses to more complex configurations.
- Specify a prefix with `@configclass(prefix="<PREFIX>")` to append this prefix to your configclass'  attribute names.
- Config groups (__TODO__): https://cli.dev/docs/tutorial/config_groups/

## Requirements

Python 3.8+


## Installation

Depending on your chosen config file format you can install:

- .env  ->   ```pip install 12factor-configclasses[dotenv]```
- .yaml ->   ```pip install 12factor-configclasses[yaml]```
- .toml ->   ```pip install 12factor-configclasses[toml]```
- .ini  ->   ```pip install 12factor-configclasses```
- .json ->   ```pip install 12factor-configclasses```

Or install all supported formats with:

    pip install 12factor-configclasses[full]
    
## Usage

There are three ways to use it:

- Loading an .env file:

```.env
# .env
HOST=0.0.0.0
PORT=8000
DB_URL=sqlite://:memory:
GENERATE_SCHEMAS=True
DEBUG=True
HTTPS_ONLY=False
GZIP=True
SENTRY=False
```

```python
#config.py
from configclasses import configclass


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
```

```python
# app.py
from api.config import AppConfig

app_config = AppConfig.from_path(".env")
app = Starlette(debug=app_config.debug)

if app_config.https_only:
    app.add_middleware(
        HTTPSRedirectMiddleware)
if app_config.gzip:
    app.add_middleware(GZipMiddleware)
if app_config.sentry:
    app.add_middleware(SentryAsgiMiddleware)

...

register_tortoise(
    app,
    db_url=app_config.db.url,
    modules={"models": ["api.models"]},
    generate_schemas=app_config.generate_schemas,
)

if __name__ == "__main__":
    uvicorn.run(app, host=app_config.host, port=app_config.port)
```

    
- Loading predefined environmental variables:

The same than before, but instead of:

    app_config = AppConfig.from_path(".env")
    
You will do:

    app_config = AppConfig.from_environ()
    
- Loading a file from a string:

```python
test_env = """HOST=0.0.0.0
PORT=8000
DB_URL=sqlite://:memory:
GENERATE_SCHEMAS=True
DEBUG=True
HTTPS_ONLY=False
GZIP=True
SENTRY=False"""
app_config = AppConfig.from_string(test_env, ".env")
```
