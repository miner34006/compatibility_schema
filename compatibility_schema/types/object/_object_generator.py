import random
from typing import Any

from blahblah import Generator
from niltype import Nil

from .._number_schema import NumberSchema
from ..string._string_schema import StringSchema
from ._object_schema import ObjectSchema

__all__ = ("ObjectGenerator",)

PRIMITIVES = (
    NumberSchema().integer,
    NumberSchema().float,
    StringSchema()
)


class ObjectGenerator(Generator, extend=True):
    def __get_length(self, schema):
        if schema.props.length is not Nil:
            return schema.props.length

        min_length, max_length = 0, 64

        if schema.props.get('contains') is not Nil or schema.props.get('contains_one') is not Nil:
            min_length = 1
        if schema.props.get('contains_many') is not Nil:
            min_length = 2
        if schema.props.get('contains_all') is not Nil:
            min_length = len(schema.props.contains_all)

        if schema.props.get('min_length') is not Nil:
            min_length = schema.props.min_length
        if schema.props.get('max_length') is not Nil:
            max_length = schema.props.max_length

        max_length = max([min_length, max_length])
        return random.randint(min_length, max_length)

    def __get_object_key(self):
        return StringSchema().alphabetic.lowercase.length(1).__accept__(self) + \
            StringSchema().alpha_num.lowercase.length(1, 15).__accept__(self)

    def visit_object(self, schema: ObjectSchema, **kwargs: Any) -> str:
        obj = {}
        if schema.props.keys is not Nil:
            for key, item_schema in schema.props.keys.items():
                is_required = item_schema[1]
                if is_required:
                    obj[key] = item_schema[0].__accept__(self, **kwargs)

        if (schema.props.keys is Nil) or (len(schema.props.keys) > 0):
            if len(obj) == 0 or any(x in schema.props for x in ['length', 'min_length', 'max_length']):
                length = self.__get_length(schema) - len(obj)
                for _ in range(length):
                    key = self.__get_object_key()
                    obj[key] = random.choice(PRIMITIVES).__accept__(self)

        return obj
