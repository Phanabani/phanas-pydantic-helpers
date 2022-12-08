# Phana's Pydantic Helpers

[![release](https://img.shields.io/github/v/release/phanabani/phanas-pydantic-helpers)](https://github.com/phanabani/phanas-pydantic-helpers/releases)
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

To get started, install the repo with Poetry.

```shell
poetry add "https://github.com/phanabani/phanas-pydantic-helpers.git"
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
