from typing import Any, Dict, List
from unittest.mock import patch

from pydantic import BaseModel
import pytest
from typing_extensions import Protocol

from phanas_pydantic_helpers import (
    Factory,
    FieldConverter,
    create_template_from_model,
)
from phanas_pydantic_helpers.helpers import create_template_model_module


@pytest.fixture(autouse=True)
def patch_PLACEHOLDER_DICT_KEY_STR():
    with patch.object(
        create_template_model_module,
        "PLACEHOLDER_DICT_KEY_STR",
        "__TESTING_PLACEHOLDER_DICT_KEY_STR__",
    ) as placeholder:
        yield placeholder


@pytest.fixture()
def phana():
    return "Phana"


@pytest.fixture()
def user_id():
    return 123


class TestBasic:
    def test_empty(self):
        class Model(BaseModel):
            pass

        assert create_template_from_model(Model) == {}

    def test_annotation_only(self):
        class Model(BaseModel):
            name: str

        assert create_template_from_model(Model) == {"name": "NAME"}

    def test_value_only(self, phana):
        class Model(BaseModel):
            name = phana

        assert create_template_from_model(Model) == {"name": phana}

    def test_annotation_and_value(self, phana):
        class Model(BaseModel):
            name: str = phana

        assert create_template_from_model(Model) == {"name": phana}


class TestList:
    def test_annotation_only(self):
        class Model(BaseModel):
            name: List[str]

        assert create_template_from_model(Model) == {"name": ["NAME"]}

    def test_value_only(self, phana):
        class Model(BaseModel):
            name = [phana]

        assert create_template_from_model(Model) == {"name": [phana]}

    def test_annotation_and_value(self, phana):
        class Model(BaseModel):
            name: List[str] = [phana]

        assert create_template_from_model(Model) == {"name": [phana]}


class TestDict:
    def test_annotation_only_str_int(self, patch_PLACEHOLDER_DICT_KEY_STR):
        class Model(BaseModel):
            name_to_id: Dict[str, int]

        assert create_template_from_model(Model) == {
            "name_to_id": {patch_PLACEHOLDER_DICT_KEY_STR: 0}
        }

    def test_annotation_only_int_str(self):
        class Model(BaseModel):
            id_to_name: Dict[int, str]

        assert create_template_from_model(Model) == {"id_to_name": {0: "ID_TO_NAME"}}

    def test_value_only(self, phana, user_id):
        class Model(BaseModel):
            name_to_id = {phana: user_id}

        assert create_template_from_model(Model) == {"name_to_id": {phana: user_id}}

    def test_annotation_and_value_str_int(self, phana, user_id):
        class Model(BaseModel):
            name_to_id: Dict[str, int] = {phana: user_id}

        assert create_template_from_model(Model) == {"name_to_id": {phana: user_id}}

    def test_annotation_and_value_int_str(self, phana, user_id):
        class Model(BaseModel):
            id_to_name: Dict[int, str] = {user_id: phana}

        assert create_template_from_model(Model) == {"id_to_name": {user_id: phana}}


class TestModelNoDefault:
    @pytest.fixture()
    def person_cls(self):
        class Person(BaseModel):
            name: str

        return Person

    def test_annotation_only(self, person_cls, patch_PLACEHOLDER_DICT_KEY_STR):
        class Model(BaseModel):
            person: person_cls

        assert create_template_from_model(Model) == {"person": {"name": "NAME"}}

    def test_annotation_and_value(self, person_cls):
        class Model(BaseModel):
            person: person_cls = Factory(person_cls)

        assert create_template_from_model(Model) == {"person": {"name": "NAME"}}


class TestModelWithDefault:
    @pytest.fixture()
    def person_cls(self, phana):
        class Person(BaseModel):
            name: str = phana

        return Person

    def test_annotation_only(self, person_cls, phana):
        class Model(BaseModel):
            person: person_cls

        assert create_template_from_model(Model) == {"person": {"name": phana}}

    def test_annotation_and_value(self, person_cls, phana):
        class Model(BaseModel):
            person: person_cls = Factory(person_cls)

        assert create_template_from_model(Model) == {"person": {"name": phana}}


def test_complex(patch_PLACEHOLDER_DICT_KEY_STR):
    class Player(BaseModel):
        name: str
        admin = False
        highest_score: float = 1.0
        extra_data: Dict[str, str]

    class PlayerDatabase(BaseModel):
        version: int
        players: List[Player]

    class GameSystem(BaseModel):
        system_name = "PhanaBox"
        games: List[str]
        player_database: PlayerDatabase = Factory(PlayerDatabase)

    assert create_template_from_model(GameSystem) == {
        "system_name": "PhanaBox",
        "games": ["GAMES"],
        "player_database": {
            "version": 0,
            "players": [
                {
                    "name": "NAME",
                    "admin": False,
                    "highest_score": 1.0,
                    "extra_data": {patch_PLACEHOLDER_DICT_KEY_STR: "EXTRA_DATA"},
                }
            ],
        },
    }


class TestFieldConverter:
    def test_str(self):
        class Container:
            def __init__(self, value: Any):
                self.value = value

        class StrToContainer(Container, FieldConverter):
            @classmethod
            def _pyd_convert(cls, value: str):
                return cls(value)

        class Model(BaseModel):
            str_to_container: StrToContainer

        assert create_template_from_model(Model) == {
            "str_to_container": "STR_TO_CONTAINER"
        }

    def test_int(self):
        class Container:
            def __init__(self, value: Any):
                self.value = value

        class IntToContainer(Container, FieldConverter):
            @classmethod
            def _pyd_convert(cls, value: int):
                return cls(value)

        class Model(BaseModel):
            int_to_container: IntToContainer

        assert create_template_from_model(Model) == {"int_to_container": 0}

    def test_allow_any_arg_name(self):
        class Container:
            def __init__(self, _testing_arg_name_: Any):
                self._testing_arg_name_ = _testing_arg_name_

        class IntToContainer(Container, FieldConverter):
            @classmethod
            def _pyd_convert(cls, _testing_arg_name_: int):
                return cls(_testing_arg_name_)

        class Model(BaseModel):
            int_to_container: IntToContainer

        assert create_template_from_model(Model) == {"int_to_container": 0}

    def test_gets_type_of_first_converter_only(self):
        class Container:
            def __init__(self, value: Any):
                self.value = value

        class ToContainer(Container, FieldConverter):
            # Ensuring that alphabetical order doesn't matter, only definition
            # order
            @classmethod
            def _pyd_convert_b_int(cls, value: int):
                return cls(value)

            @classmethod
            def _pyd_convert_a_str(cls, value: str):
                return cls(value)

        class Model(BaseModel):
            to_container: ToContainer

        assert create_template_from_model(Model) == {"to_container": 0}

    def test_mro(self):
        class ContainerProto(Protocol):
            value: int

        class Container(ContainerProto):
            def __init__(self, value: int):
                self.value = value

        class IntToContainerProtoImpl(Container, FieldConverter):
            @classmethod
            def _pyd_convert(cls, value: int):
                return cls(value)

        class Model(BaseModel):
            int_to_container_proto_impl: IntToContainerProtoImpl

        assert create_template_from_model(Model) == {"int_to_container_proto_impl": 0}
