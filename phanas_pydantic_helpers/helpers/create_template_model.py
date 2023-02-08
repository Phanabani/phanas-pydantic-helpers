from __future__ import annotations

__all__ = ["create_template_model"]

import sys
from typing import TypeVar, get_type_hints

from pydantic import BaseModel

# noinspection PyProtectedMember
from pydantic.main import ModelMetaclass
from typing_extensions import get_args, get_origin

T = TypeVar("T")

PLACEHOLDER_DICT_KEY_STR = "NAME"

templatable_types = (list, dict, BaseModel)


def create_template_by_type(type_: type[T], field_name: str) -> T:
    if isinstance(type_, ModelMetaclass):
        return create_template_model(type_)

    if type_ is str:
        return field_name.upper()

    origin_type = get_origin(type_)

    if origin_type is dict:
        key_type, value_type = get_args(type_)
        if key_type is str:
            placeholder_key = PLACEHOLDER_DICT_KEY_STR
        else:
            placeholder_key = key_type()
        return {placeholder_key: create_template_by_type(value_type, field_name)}

    if origin_type is list:
        item_type = get_args(type_)[0]
        return [create_template_by_type(item_type, field_name)]

    return type_()


def create_template_model(
    model_type: type[BaseModel] | ModelMetaclass,
) -> dict[str, object]:
    dict_ = {}
    annotations = get_type_hints(
        model_type, vars(sys.modules[model_type.__module__]), vars(model_type)
    )
    for field_name, field in model_type.__fields__.items():
        if not field.required:
            factory = field.default_factory
            if field_name in annotations and (
                factory in templatable_types or isinstance(factory, ModelMetaclass)
            ):
                value = create_template_by_type(annotations[field_name], field_name)
            else:
                value = factory() if factory else field.default
        else:
            value = create_template_by_type(field.type_, field_name)
        dict_[field_name] = value

    return dict_
