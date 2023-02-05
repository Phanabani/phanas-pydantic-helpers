from __future__ import annotations

__all__ = ["raise_if_missing_deps", "DummyModule"]

from typing import Any

from typing_extensions import Self


def raise_if_missing_deps(*modules: Any) -> None:
    missing_dep_names = []

    for module in modules:
        if isinstance(module, DummyModule):
            missing_dep_names.append(str(module))

    if missing_dep_names:
        raise ImportError(f"Missing modules {missing_dep_names}")


class DummyModule:
    def __init__(self, module_name: str):
        self.__dummy_module__module_name = module_name

    def __str__(self):
        return self.__dummy_module__module_name

    def __repr__(self):
        return f"DummyModule({self.__dummy_module__module_name})"

    def __getattr__(self, item: str) -> Self:
        return self

    def __call__(self, *args, **kwargs) -> Self:
        return self

    def __mro_entries__(self, bases):
        return ()
