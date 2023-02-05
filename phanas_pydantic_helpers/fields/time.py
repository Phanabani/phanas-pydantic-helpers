from __future__ import annotations

__all__ = ["DateTimeField", "TimeField", "DurationField"]

from phanas_pydantic_helpers.common.imports import DummyModule, raise_if_missing_deps
from phanas_pydantic_helpers.common.time import parse_duration, parse_time
from phanas_pydantic_helpers.helpers import FieldConverter

try:
    import pendulum as pen
except ImportError:
    pen = DummyModule("pendulum")


class DateTimeField(pen.DateTime, FieldConverter):
    @classmethod
    def _pyd_convert(cls, datetime_str: str):
        raise_if_missing_deps(pen)

        parsed_dt = pen.parse(datetime_str)
        if not isinstance(parsed_dt, pen.DateTime):
            raise ValueError("Invalid datetime format")
        return parsed_dt


class TimeField(pen.Time, FieldConverter):
    @classmethod
    def _pyd_convert(cls, time_str: str):
        raise_if_missing_deps(pen)
        return parse_time(time_str, class_=cls)


class DurationField(pen.Duration, FieldConverter):
    @classmethod
    def _pyd_convert(cls, duration_str: str):
        raise_if_missing_deps(pen)
        return parse_duration(duration_str, class_=cls)
