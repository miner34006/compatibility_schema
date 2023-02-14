from typing import Any

from niltype import Nil
from revolt import Substitutor
from revolt.errors import make_substitution_error

from ._string_schema import StringSchema

__all__ = ("StringSubstitutor",)


class StringSubstitutor(Substitutor, extend=True):
    def visit_string(self, schema: StringSchema, *,
                     value: Any = Nil, **kwargs: Any) -> StringSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))
