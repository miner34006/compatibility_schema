from typing import Any

from niltype import Nil
from revolt import Substitutor

from ._string_schema import StringSchema

__all__ = ("StringSubstitutor",)


class StringSubstitutor(Substitutor, extend=True):
    def visit_string(self, schema: StringSchema, *,
                     value: Any = Nil, **kwargs: Any) -> StringSchema:
        return schema.__class__(schema.props.update(value=value))
