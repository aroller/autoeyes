from abc import ABCMeta, abstractmethod
from collections import Iterable
from typing import List

from connexion.operations import abstract


class ApiModel(metaclass=ABCMeta):
    """Any object that wishes to be represented as json in an API."""

    @abstractmethod
    def api_json(self):
        pass

    @staticmethod
    def to_json(o: object):
        if isinstance(o, (list,)):
            return ApiModel.list_to_json(o)
        elif isinstance(o, dict):
            return ApiModel.dict_to_json(o)
        elif isinstance(o, ApiModel):
            return o.api_json()
        elif isinstance(o, Iterable):
            return ApiModel.list_to_json(o)
        else:
            return o.__dict__


    @staticmethod
    def list_to_json(objects: List):
        json = []
        for o in objects:
            json.append(ApiModel.to_json(o))
        return json

    @staticmethod
    def dict_to_json(o: dict):
        json = {}
        for key in o.keys():
            value = o[key]
            json[key] = ApiModel.to_json(value)
        return json
