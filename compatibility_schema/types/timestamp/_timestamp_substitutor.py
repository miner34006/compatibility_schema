from typing import Any

from niltype import Nil
from revolt import Substitutor

from ._timestamp_schema import TimestampSchema

__all__ = ("TimestampSubstitutor",)


class TimestampSubstitutor(Substitutor, extend=True):
    def visit_timestamp(self, schema: TimestampSchema, *,
                        value: Any = Nil, **kwargs: Any) -> TimestampSchema:
        return schema.__class__(schema.props.update(value=value))
