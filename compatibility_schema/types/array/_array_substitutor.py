from typing import Any

from niltype import Nil
from revolt import Substitutor
from revolt.errors import SubstitutionError, make_substitution_error

from district42 import from_native

from ...helpers import check_type
from ._array_schema import ArraySchema

__all__ = ("ArraySubstitutor",)


class ArraySubstitutor(Substitutor, extend=True):
    def visit_array(self, schema: ArraySchema, *,
                    value: Any = Nil, **kwargs: Any) -> ArraySchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)

        error = check_type(value, [list])
        if error:
            raise SubstitutionError(error)

        array_items = []
        if schema.props.items is not Nil:
            for idx, item in enumerate(schema.props.items):
                array_items += [item % value[idx]]
        else:
            for item in value:
                array_items += [from_native(item)]

        return schema.__class__(schema.props.update(items=array_items))


