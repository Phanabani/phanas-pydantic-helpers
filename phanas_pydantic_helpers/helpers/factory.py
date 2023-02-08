__all__ = ["Factory", "instance_list_factory"]

from typing import Callable, List, Type, TypeVar

from pydantic.fields import FieldInfo

V = TypeVar("V")


class Factory(FieldInfo):
    def __init__(self, default_factory, *args, **kwargs):
        super().__init__(*args, default_factory=default_factory, **kwargs)


def instance_list_factory(class_: Type[V], *args, **kwargs) -> Callable[[], List[V]]:
    def make_list():
        return [class_(*args, **kwargs)]

    return make_list
