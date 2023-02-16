import random
from typing import Any

from blahblah import Generator
from district42.types import Schema
from niltype import Nil

from .._number_schema import NumberSchema
from ..string._string_schema import StringSchema
from ._array_schema import ArraySchema

__all__ = ("ArrayGenerator",)


PRIMITIVES = (
    NumberSchema().integer,
    NumberSchema().float,
    StringSchema()
)

class ArrayGenerator(Generator, extend=True):
    def __get_length(self, schema):
        if schema.props.length is not Nil:
            return schema.props.length

        min_length, max_length = 0, 64

        if (schema.props.contains is not Nil) or (schema.props.contains_one is not Nil):
            min_length = 1
        if schema.props.contains_many is not Nil:
            min_length = 2
        if schema.props.contains_all:
            min_length = len(schema.props.contains_all)

        if schema.props.min_length is not Nil:
            min_length = schema.props.min_length
        if schema.props.max_length is not Nil:
            max_length = schema.props.max_length

        max_length = max([min_length, max_length])
        return random.randint(min_length, max_length)

    def visit_array(self, schema: ArraySchema, **kwargs: Any) -> str:
        if schema.props.items is not Nil:
            items = []
            for elem in schema.props.items:
                items.append(elem.__accept__(self, **kwargs))
            return items

        length = self.__get_length(schema)
        if (schema.props.contains_one is not Nil) or (schema.props.contains_all is not Nil):
            items = None
            if schema.props.contains_all is not Nil:
                items = schema.props.contains_all
            else:
                items = [schema.props.contains_one]
            array = [item.__accept__(self) for item in items]
            while len(array) < length:
                primitive = random.choice(PRIMITIVES).__accept__(self)
                if primitive not in array:
                    array.append(primitive)
            if length > 1:
                index = random.randint(1, length - 1)
                array[0], array[index] = array[index], array[0]
            return array

        array = []
        if schema.props.contains is not Nil:
            count = random.randint(1, length)
            array += [schema.props.contains.__accept__(self) for _ in range(count)]
        elif schema.props.contains_many is not Nil:
            count = random.randint(2, length)
            array += [schema.props.contains_many.__accept__(self) for _ in range(count)]

        length -= len(array)
        return array + [random.choice(PRIMITIVES).__accept__(self) for _ in range(length)]
