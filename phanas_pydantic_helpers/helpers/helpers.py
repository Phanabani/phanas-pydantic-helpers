__all__ = [
    "FieldConverterError",
    "FieldConverter",
    "update_forward_refs_recursive",
]

from typing import Any, Callable, Dict, Type, TypeVar

from pydantic import BaseModel

from phanas_pydantic_helpers.common.typing import (
    get_function_args_annotations,
)


class FieldConverterError(Exception):
    pass


T_Converter = Callable[[Type["FieldConverterBase"], Any], Any]


class FieldConverter:
    """
    Examples:

        class TimezoneField(Timezone, FieldConverter):
            @classmethod
            def _pyd_convert_str(cls, timezone_str: str):
                return cls(timezone_str)

            @classmethod
            def _pyd_convert_timezone(cls, timezone: Timezone):
                return cls(timezone.name)


        class TimeField(pen.Time, FieldConverter):
            @classmethod
            def _pyd_convert(cls, time_str: str):
                return parse_time(time_str, class_=cls)
    """

    __pyd_converters: Dict[type, T_Converter] = None
    __pyd_converter_prefix = "_pyd_convert"

    @classmethod
    def __get_validators__(cls):
        yield cls.__pyd_convert

    @classmethod
    def __pyd_get_converters(cls) -> Dict[type, T_Converter]:
        if cls.__pyd_converters is not None:
            return cls.__pyd_converters

        converters: Dict[type, T_Converter] = {}
        for name, member in cls.__dict__.items():
            # Iterate through this class's members and find converter methods
            if not isinstance(member, classmethod):
                continue
            if not name.startswith(cls.__pyd_converter_prefix):
                continue

            # Check that the converter method has a single value argument and
            # that the type doesn't already have a converter
            fn = member.__func__  # Unwrap classmethod
            fn_args_types = list(get_function_args_annotations(fn).values())
            if len(fn_args_types) != 1:
                raise FieldConverterError(
                    f"Converter {name} must take one positional argument: value"
                )
            converter_type = fn_args_types[0]
            if converter_type in converters:
                raise FieldConverterError(
                    f"Multiple converters found for type {converter_type}, there "
                    f"should only be one"
                )
            converters[converter_type] = fn

        cls.__pyd_converters = converters
        return cls.__pyd_converters

    @classmethod
    def __pyd_convert(cls, value):
        converters = cls.__pyd_get_converters()
        try:
            fn = converters[type(value)]
        except KeyError:
            raise TypeError(f"No converter for type {type(value)}")
        return fn(cls, value)


T_BaseModel = TypeVar("T_BaseModel", bound=Type[BaseModel])


def update_forward_refs_recursive(model: T_BaseModel) -> T_BaseModel:
    for name, value in model.__dict__.items():
        if isinstance(value, type) and issubclass(value, BaseModel):
            update_forward_refs_recursive(value)

    model.update_forward_refs(**model.__dict__)
    return model
