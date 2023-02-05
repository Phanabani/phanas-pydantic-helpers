from __future__ import annotations

__all__ = ["requires", "DummyModule"]

from functools import wraps
import sys
from types import FunctionType
from typing import Optional, TypeVar, cast

from phanas_pydantic_helpers.common.constants import pypi_package_name

T_FunctionOrClass = TypeVar("T_FunctionOrClass", bound=FunctionType | type)


def requires(*required_module_names: str, extra_name: Optional[str] = None):
    def wrapper(fn_or_cls: T_FunctionOrClass) -> T_FunctionOrClass:
        modules_were_checked = False

        def check_module_imported():
            nonlocal modules_were_checked

            print("Beginning import check")

            if not modules_were_checked:
                missing_modules = []
                for required_module in required_module_names:
                    print(f"Checking: {required_module}")
                    if required_module not in sys.modules:
                        print(f"{required_module} missing!")
                        missing_modules.append(required_module)

                if missing_modules:
                    msg = f"Missing required modules: {missing_modules}"
                    if extra_name:
                        msg += (
                            f". Install with pip install "
                            f"{pypi_package_name}[{extra_name}]"
                        )
                    raise ImportError(msg)

                modules_were_checked = True

        if isinstance(fn_or_cls, FunctionType):

            @wraps(fn_or_cls)
            def wrapped(*args, **kwargs):
                check_module_imported()
                return fn_or_cls(*args, **kwargs)

            print(f"Returning wrapped fn {fn_or_cls.__name__}")
            return cast(T_FunctionOrClass, wrapped)

        elif isinstance(fn_or_cls, type):

            class Wrapped(fn_or_cls):
                @wraps(fn_or_cls.__init__)
                def __init__(self, *args, **kwargs):
                    print("")
                    check_module_imported()
                    super().__init__(*args, **kwargs)

                @wraps(fn_or_cls.__getattribute__)
                def __getattribute__(self, item):
                    check_module_imported()
                    super().__init__(item)

            print(f"Returning wrapped class {fn_or_cls.__name__}")
            return Wrapped

    return wrapper


class DummyModule:
    def __getattr__(self, item: str) -> DummyModule:
        return DummyModule()

    def __call__(self, *args, **kwargs) -> DummyModule:
        return DummyModule()

    def __mro_entries__(self, bases):
        return ()
