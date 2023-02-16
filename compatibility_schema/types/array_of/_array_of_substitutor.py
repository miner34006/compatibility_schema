from typing import Any

from niltype import Nil
from revolt import Substitutor
from revolt.errors import SubstitutionError

from ...helpers import check_type
from ..array import ArraySchema
from ._array_of_schema import ArrayOfSchema

__all__ = ("ArrayOfSubstitutor",)


class ArrayOfSubstitutor(Substitutor, extend=True):
    def visit_array_of(self, schema: ArrayOfSchema, *,
                    value: Any = Nil, **kwargs: Any) -> ArrayOfSchema:
        error = check_type(value, [list])
        if error:
            raise SubstitutionError(error)

        array_items = []
        for item in value:
            array_items += [schema.props.type % item]

        return ArraySchema()(array_items)
