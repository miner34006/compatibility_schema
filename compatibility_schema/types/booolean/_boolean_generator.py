from typing import Any

from blahblah import Generator
from niltype import Nil

from ._boolean_schema import BooleanSchema

__all__ = ("BooleanGenerator",)


class BooleanGenerator(Generator, extend=True):
    def visit_boolean(self, schema: BooleanSchema, **kwargs: Any) -> str:
        if schema.props.value is not Nil:
            return schema.props.value
        return self._random.random_choice((True, False))
