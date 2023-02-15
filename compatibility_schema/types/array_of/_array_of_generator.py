import random
from typing import Any

from blahblah import Generator
from niltype import Nil

from . import ArrayOfSchema

__all__ = ("ArrayOfGenerator",)


class ArrayOfGenerator(Generator, extend=True):
    def __get_length(self, schema):
        if schema.props.length is not Nil:
            return schema.props.length

        min_length, max_length = 0, 64
        if schema.props.min_length is not Nil:
            min_length = schema.props.min_length
        if schema.props.max_length is not Nil:
            max_length = schema.props.max_length

        max_length = max([min_length, max_length])
        return random.randint(min_length, max_length)

    def visit_array_of(self, schema: ArrayOfSchema, **kwargs: Any) -> str:
        length = self.__get_length(schema)
        return [schema.props.type.__accept__(self) for _ in range(length)]
