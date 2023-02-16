from typing import Any

from district42.representor import Representor
from niltype import Nil

from ..object._object_schema import ObjectSchema
from ._array_of_schema import ArrayOfSchema

__all__ = ("ArrayOfRepresentor",)


class ArrayOfRepresentor(Representor, extend=True):
    def __is_indentable(self, schema):
        from .. import ArraySchema
        return type(schema) in [ObjectSchema, ArraySchema]

    def visit_array_of(self, schema: ArrayOfSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.array_of"

        items_schema = schema.props.type
        if self.__is_indentable(items_schema):
            r += '({})'.format(items_schema.__accept__(self, indent=indent))
        else:
            r += '({})'.format(items_schema.__accept__(self))

        if schema.props.empty is not Nil:
            r += '.empty' if schema.props.empty else '.non_empty'
        elif schema.props.length is not Nil:
            r += '.length({})'.format(schema.props.length)
        elif schema.props.min_length is not Nil and schema.props.max_length is not Nil:
            r += '.length({}, {})'.format(
                schema.props.min_length,
                schema.props.max_length
            )
        elif schema.props.min_length is not Nil:
            r += '.min_length({})'.format(schema.props.min_length)
        elif schema.props.max_length is not Nil:
            r += '.max_length({})'.format(schema.props.max_length)

        return r
