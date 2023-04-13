from typing import Any

from niltype import Nil
from revolt import Substitutor
from revolt.errors import SubstitutionError

from ...helpers import check_type
from ._string_schema import StringSchema

__all__ = ("StringSubstitutor",)


class StringSubstitutor(Substitutor, extend=True):
    def visit_string(self, schema: StringSchema, *,
                     value: Any = Nil, **kwargs: Any) -> StringSchema:
        error = check_type(value, [str])
        if error:
            raise SubstitutionError(error)
        return schema.__class__(schema.props.update(
            value=value
        ))
