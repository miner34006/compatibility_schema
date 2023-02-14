from typing import Any

from niltype import Nil

from district42.representor import Representor

from ._array_schema import ArraySchema
from ..object._object_schema import ObjectSchema

__all__ = ("ArrayRepresentor",)


class ArrayRepresentor(Representor, extend=True):
    def __is_indentable(self, schema):
        return type(schema) in [ObjectSchema, ArraySchema]

    def __get_array_items(self, items, indent):
        for item in items:
            if self.__is_indentable(item):
                yield item.__accept__(self, indent=indent)
            else:
                yield item.__accept__(self)

    def visit_array(self, schema: ArraySchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.array"

        if schema.props.items is not Nil:
            items = schema.props.items
            if len(items) <= 2:
                r += '([{}])'.format(', '.join(self.__get_array_items(items, indent)))
            else:
                spaces = ' ' * (indent + self._indent)
                separator = ',\n' + spaces
                r += '([\n{}{}\n])'.format(
                    spaces,
                    separator.join(self.__get_array_items(items, indent + self._indent))
                )
        elif schema.props.contains is not Nil:
            r += '.contains'
            item = schema.props.contains
            if self.__is_indentable(item):
                r += '({})'.format(item.__accept__(self, indent=indent))
            else:
                r += '({})'.format(item.__accept__(self))
        elif schema.props.contains_one is not Nil:
            r += '.contains_one'
            item = schema.props.contains_one
            if self.__is_indentable(item):
                r += '({})'.format(item.__accept__(self, indent=indent))
            else:
                r += '({})'.format(item.__accept__(self))
        elif schema.props.contains_many is not Nil:
            r += '.contains_many'
            item = schema.props.contains_many
            if self.__is_indentable(item):
                r += '({})'.format(item.__accept__(self, indent=indent))
            else:
                r += '({})'.format(item.__accept__(self))
        elif schema.props.contains_all is not Nil:
            items = schema.props.contains_all
            r += '.contains_all([{}])'.format(', '.join(item.__accept__(self) for item in items))

        if schema.props.empty is not Nil:
            r += '.empty' if schema.props.empty else '.non_empty'
        elif schema.props.length is not Nil:
            r += '.length({})'.format(schema.props.length)
        elif (schema.props.min_length is not Nil) and (schema.props.max_length is not Nil):
            r += '.length({}, {})'.format(
                schema.props.min_length,
                schema.props.max_length
            )
        elif schema.props.min_length is not Nil:
            r += '.min_length({})'.format(schema.props.min_length)
        elif schema.props.max_length is not Nil:
            r += '.max_length({})'.format(schema.props.max_length)

        return r
