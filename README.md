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

from phanas_pydantic_helpers import update_forward_refs_recursive, Factory


@update_forward_refs_recursive
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

## Developers

### Installation

Follow the installation steps in [install](#install) and use Poetry to 
install the development dependencies:

```shell
poetry install
```

## License

[MIT © Phanabani.](LICENSE)
