from pydantic import BaseModel

from phanas_pydantic_helpers import FieldConverter


def test_basic():
    class StrToInt(int, FieldConverter):
        @classmethod
        def _pyd_convert(cls, value: str) -> int:
            return int(value)

    class Model(BaseModel):
        x: StrToInt

    m = Model(x="5")
    assert m.x == 5


def test_basic_with_suffix():
    class StrToInt(int, FieldConverter):
        @classmethod
        def _pyd_convert_str(cls, value: str) -> int:
            return int(value)

    class Model(BaseModel):
        x: StrToInt

    m = Model(x="5")
    assert m.x == 5


def test_multiple_converters():
    class ToInt(int, FieldConverter):
        @classmethod
        def _pyd_convert_str(cls, value: str) -> int:
            return int(value)

        @classmethod
        def _pyd_convert_bytes(cls, value: bytes) -> int:
            return int.from_bytes(value, "big")

    class Model(BaseModel):
        x: ToInt

    m_str = Model(x="5")
    assert m_str.x == 5

    m_bytes = Model(x=b"\x00\xFF")
    assert m_bytes.x == 0xFF
