__all__ = ["update_forward_refs_recursive"]

from typing import Type, TypeVar

from pydantic import BaseModel

T_BaseModel = TypeVar("T_BaseModel", bound=Type[BaseModel])


def update_forward_refs_recursive(model: T_BaseModel) -> T_BaseModel:
    for name, value in model.__dict__.items():
        if isinstance(value, type) and issubclass(value, BaseModel):
            update_forward_refs_recursive(value)

    model.update_forward_refs(**model.__dict__)
    return model
