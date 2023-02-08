# Phana's Pydantic Helpers

[![pypi](https://img.shields.io/pypi/v/phanas-pydantic-helpers)]()
[![pypi-python](https://img.shields.io/pypi/pyversions/phanas-pydantic-helpers)]()
[![license](https://img.shields.io/github/license/phanabani/phanas-pydantic-helpers)](LICENSE)

A collection of helper functions/classes for Pydantic.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Developers](#developers)
- [License](#license)

## Install

### Prerequisites

- [Poetry](https://python-poetry.org/docs/#installation) – dependency manager

### Install Phana's Pydantic Helpers

To get started, install the package with Poetry.

```shell
poetry add phanas-pydantic-helpers
```

## Usage

### `Factory` and `update_forward_refs_recursive`

`Factory(...)` is simply an alias for `pydantic.Field(default_factory=...).`

```python
from pydantic import BaseModel

from phanas_pydantic_helpers import Factory


class Config(BaseModel):
    token: str
    
    class _ExtraInfo(BaseModel):
        name: str = "Unnamed"
        description: str = "Empty description"

    extra_info: _ExtraInfo = Factory(_ExtraInfo)


model = Config(token="bleh")
assert model.extra_info.name == "Unnamed"
model.extra_info.description = "A more detailed description"
```

### `FieldConverter`

Easily create custom fields with one or more type converters. Make sure the
first superclass is the type you want to represent, as this is considered
the main base class and will take precedence over FieldConverter, offering
better code completion.

```python
from phanas_pydantic_helpers import FieldConverter
from pydantic import BaseModel


class ToInt(int, FieldConverter):

    @classmethod
    def _pyd_convert_str(cls, value: str) -> int:
        return int(value)

    @classmethod
    def _pyd_convert_bytes(cls, value: bytes) -> int:
        return int.from_bytes(value, "big")


class Container(BaseModel):
    value: ToInt


container_from_str = Container(value="5")
assert container_from_str.value == 5

container_from_bytes = Container(value=b"\x00\xFF")
assert container_from_bytes.value == 0xFF
```

### `create_template_from_model`

Create a dict from a model with required fields. This function fills in required
fields with placeholders.

```python
from typing import Dict, List

from pydantic import BaseModel
from phanas_pydantic_helpers import Factory, create_template_from_model


class Player(BaseModel):
    name: str
    admin = False
    highest_score: float = 1.0
    extra_data: Dict[str, str]


class PlayerDatabase(BaseModel):
    version: int
    players: List[Player]


class GameSystem(BaseModel):
    system_name = "PhanaBox"
    games: List[str]
    player_database: PlayerDatabase = Factory(PlayerDatabase)


assert create_template_from_model(GameSystem) == {
    "system_name": "PhanaBox",
    "games": ["GAMES"],
    "player_database": {
        "version": 0,
        "players": [
            {
                "name": "NAME",
                "admin": False,
                "highest_score": 1.0,
                "extra_data": {"KEY_NAME": "EXTRA_DATA"},
            }
        ],
    },
}
```

## Developers

### Installation

Follow the installation steps in [install](#install) and use Poetry to 
install the development dependencies:

```shell
poetry install
```

## License

[MIT © Phanabani.](LICENSE)
