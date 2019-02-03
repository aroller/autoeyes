import unittest
from enum import Enum, auto

from api_model import ApiModelSerializer


class TestEnumForApiModel(Enum):
    a = auto()
    b = auto()
    c = auto()


class ApiModelSerializerTest(unittest.TestCase):

    def test_enum_serializer(self):
        result = ApiModelSerializer.to_json(TestEnumForApiModel.a)
        self.assertEqual(result, TestEnumForApiModel.a.name)

