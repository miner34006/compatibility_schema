from typing import Any

from district42.representor import Representor
from niltype import Nil

from ..array import ArraySchema
from ._object_schema import ObjectSchema

__all__ = ("ObjectRepresentor",)


class ObjectRepresentor(Representor, extend=True):
    def __is_indentable(self, schema):
        return type(schema) in [ObjectSchema, ArraySchema]

    def __get_object_keys(self, items, indent):
        keys = []
        for key, val in items:
            actual_val = val[0]
            if self.__is_indentable(actual_val):
                _repr = actual_val.__accept__(self, indent=indent)
            else:
                _repr = actual_val.__accept__(self)
            keys.append("{}'{}': {}".format(' ' * indent, key, _repr))
        return keys

    def visit_object(self, schema: ObjectSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.object"

        if schema.props.keys is not Nil:
            if len(schema.props.keys) > 0:
                r += '({\n'
                sorted_items = sorted(schema.props.keys.items())
                keys = self.__get_object_keys(sorted_items, indent + self._indent)
                r += ',\n'.join(keys) + '\n' + (' ' * indent) + '})'
            else:
                r += '({})'

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

        if schema.props.strict is not Nil:
            r += '.strict'

        return r
