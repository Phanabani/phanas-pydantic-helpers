from __future__ import annotations

__all__ = ["create_template_from_model"]

import sys
from typing import TypeVar, get_type_hints

from pydantic import BaseModel

# noinspection PyProtectedMember
from pydantic.main import ModelMetaclass
from typing_extensions import get_args, get_origin

from phanas_pydantic_helpers.common.typing import get_function_args_annotations
from phanas_pydantic_helpers.helpers.field_converter import (
    FieldConverter,
    CONVERTER_METHOD_PREFIX,
)

T = TypeVar("T")

PLACEHOLDER_DICT_KEY_STR = "KEY_NAME"

templatable_types = (list, dict, BaseModel)

MISSING = object()


def create_template_from_type(type_: type[T], field_name: str) -> T:
    if isinstance(type_, ModelMetaclass):
        return create_template_from_model(type_)

    # If a class inherits a `typing.Protocol`, its type will not be `type`
    # like expected, and `issubclass` will not be able to be run on it. We can
    # search for FieldConverter in __mro__ instead.
    if hasattr(type_, "__mro__") and FieldConverter in type_.__mro__:
        converters = (
            (getattr(type_, attr))
            for attr in vars(type_).keys()
            if attr.startswith(CONVERTER_METHOD_PREFIX)
        )
        # We're going to get ONLY the first converter's value type
        try:
            first_converter_type = get_function_args_annotations(next(converters))[
                "value"
            ]
        except StopIteration:
            raise ValueError(
                f'FieldConverter named "{field_name}" has no converter methods'
            )
        return create_template_from_type(
            # Avoid useless type error
            first_converter_type,  # noqa
            field_name,
        )

    if type_ is str:
        return field_name.upper()

    # Get origin type of parameterized type
    origin_type = get_origin(type_)

    if origin_type is dict:
        key_type, value_type = get_args(type_)
        if key_type is str:
            placeholder_key = PLACEHOLDER_DICT_KEY_STR
        else:
            # Get the default value for the key's type
            placeholder_key = key_type()
        return {placeholder_key: create_template_from_type(value_type, field_name)}

    if origin_type is list:
        item_type = get_args(type_)[0]
        return [create_template_from_type(item_type, field_name)]

    # Not parameterized, or some other parameterized type. Return the default
    # value for the type
    return type_()


def create_template_from_model(
    model_type: type[BaseModel] | ModelMetaclass,
) -> dict[str, object]:
    annotations = get_type_hints(
        model_type, vars(sys.modules[model_type.__module__]), vars(model_type)
    )

    dict_ = {}
    for field_name, field in model_type.__fields__.items():
        type_ = annotations.get(field_name, MISSING)

        if not field.required:
            # Field is optional, so it either has a default or a default_factory
            factory = field.default_factory
            if type_ is not MISSING and (
                # Only factories can be templatable types, since they're
                # generated at runtime
                factory in templatable_types
                or isinstance(factory, ModelMetaclass)
            ):
                # This default factory can be templated
                value = create_template_from_type(type_, field_name)
            else:
                # We can't template this default, so just use the default as-is
                value = factory() if factory else field.default

        else:
            # Field is required
            value = create_template_from_type(
                type_ if type is not MISSING else field.type_, field_name
            )

        dict_[field_name] = value

    return dict_
