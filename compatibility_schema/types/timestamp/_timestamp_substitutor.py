from typing import Any

from niltype import Nil
from revolt import Substitutor
from revolt.errors import make_substitution_error

from ._timestamp_schema import TimestampSchema

__all__ = ("TimestampSubstitutor",)


class TimestampSubstitutor(Substitutor, extend=True):
    def visit_timestamp(self, schema: TimestampSchema, *,
                        value: Any = Nil, **kwargs: Any) -> TimestampSchema:
        result = schema.__accept__(self._validator, value=value)
        if result.has_errors():
            raise make_substitution_error(result, self._formatter)
        return schema.__class__(schema.props.update(value=value))
