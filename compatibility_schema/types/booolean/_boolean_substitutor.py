from typing import Any

from niltype import Nil
from revolt import Substitutor
from revolt.errors import SubstitutionError

from ...helpers import check_type
from ._boolean_schema import BooleanSchema

__all__ = ("BooleanSubstitutor",)


class BooleanSubstitutor(Substitutor, extend=True):
    def visit_boolean(self, schema: BooleanSchema, *,
                     value: Any = Nil, **kwargs: Any) -> BooleanSchema:
        error = check_type(value, [bool])
        if error:
            raise SubstitutionError(error)
        return schema.__class__(schema.props.update(value=value))
