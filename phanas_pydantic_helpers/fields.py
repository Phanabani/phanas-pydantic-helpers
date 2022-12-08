from __future__ import annotations

__all__ = ["DateTimeField", "TimeField", "DurationField"]

import pendulum as pen

from server.common.pydantic.helpers import FieldConverter
from server.common.time import parse_duration, parse_time


class DateTimeField(pen.DateTime, FieldConverter):
    @classmethod
    def _pyd_convert(cls, datetime_str: str):
        parsed_dt = pen.parse(datetime_str)
        if not isinstance(parsed_dt, pen.DateTime):
            raise ValueError("Invalid datetime format")
        return parsed_dt


class TimeField(pen.Time, FieldConverter):
    @classmethod
    def _pyd_convert(cls, time_str: str):
        return parse_time(time_str, class_=cls)


class DurationField(pen.Duration, FieldConverter):
    @classmethod
    def _pyd_convert(cls, duration_str: str):
        return parse_duration(duration_str, class_=cls)
