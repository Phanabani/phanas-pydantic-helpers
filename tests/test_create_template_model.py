from typing import Dict, List
from unittest.mock import patch

from pydantic import BaseModel
import pytest

from phanas_pydantic_helpers import Factory, create_template_model
from phanas_pydantic_helpers.helpers import create_template_model_module


@pytest.fixture(autouse=True)
def patch_PLACEHOLDER_DICT_KEY_STR():
    with patch.object(
        create_template_model_module,
        "PLACEHOLDER_DICT_KEY_STR",
        "__TESTING_PLACEHOLDER_DICT_KEY_STR__",
    ) as placeholder:
        yield placeholder


class TestBasic:
    def test_empty(self):
        class Model(BaseModel):
            pass

        assert create_template_model(Model) == {}

    def test_annotation_only(self, patch_PLACEHOLDER_DICT_KEY_STR):
        class Model(BaseModel):
            name: str

        assert create_template_model(Model) == {"name": patch_PLACEHOLDER_DICT_KEY_STR}

    def test_value_only(self):
        class Model(BaseModel):
            name = "Phana"

        assert create_template_model(Model) == {"name": "Phana"}

    def test_annotation_and_value(self):
        class Model(BaseModel):
            name: str = "Phana"

        assert create_template_model(Model) == {"name": "Phana"}


class TestList:
    def test_annotation_only(self):
        class Model(BaseModel):
            name: List[str]

        assert create_template_model(Model) == {"name": ["NAME"]}

    def test_value_only(self):
        class Model(BaseModel):
            name = ["Phana"]

        assert create_template_model(Model) == {"name": ["Phana"]}

    def test_annotation_and_value(self):
        class Model(BaseModel):
            name: List[str] = ["Phana"]

        assert create_template_model(Model) == {"name": ["Phana"]}


class TestDict:
    def test_annotation_only_str_int(self):
        class Model(BaseModel):
            name_to_id: Dict[str, int]

        assert create_template_model(Model) == {"name_to_id": {"NAME_TO_ID": 0}}

    def test_annotation_only_int_str(self):
        class Model(BaseModel):
            id_to_name: Dict[int, str]

        assert create_template_model(Model) == {"id_to_name": {0: "ID_TO_NAME"}}

    def test_value_only(self):
        class Model(BaseModel):
            name_to_id = {"Phana": 123}

        assert create_template_model(Model) == {"name_to_id": {"Phana": 123}}

    def test_annotation_and_value_str_int(self):
        class Model(BaseModel):
            name_to_id: Dict[str, int] = {"Phana": 123}

        assert create_template_model(Model) == {"name_to_id": {"Phana": 123}}

    def test_annotation_and_value_int_str(self):
        class Model(BaseModel):
            id_to_name: Dict[int, str] = {123: "Phana"}

        assert create_template_model(Model) == {"id_to_name": {123: "Phana"}}


class TestModel:
    @pytest.fixture()
    def person_cls(self):
        class Person(BaseModel):
            name: str

        return Person

    def test_annotation_only(self, person_cls, patch_PLACEHOLDER_DICT_KEY_STR):
        class Model(BaseModel):
            person: person_cls

        assert create_template_model(Model) == {
            "person": {"name": patch_PLACEHOLDER_DICT_KEY_STR}
        }

    def test_value_only(self, person_cls):
        class Model(BaseModel):
            person = Factory(person_cls)

        assert create_template_model(Model) == {"person": {"name": "NAME"}}

    def test_annotation_and_value(self, person_cls):
        class Model(BaseModel):
            person: person_cls = Factory(person_cls)

        assert create_template_model(Model) == {"person": {"name": "NAME"}}
