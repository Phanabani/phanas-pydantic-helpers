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

```python
from pydantic import BaseModel

from phanas_pydantic_helpers import update_forward_refs_recursive, Factory


@update_forward_refs_recursive
class MyModel(BaseModel):
    hi: str = "there"

    class _Friend(BaseModel):
        whats: str = "up?"

    friend: _Friend = Factory(_Friend)


model = MyModel()
assert model.friend.whats == "up?"
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
