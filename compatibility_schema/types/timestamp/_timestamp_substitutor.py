from typing import Any

from niltype import Nil
from revolt import Substitutor
from revolt.errors import SubstitutionError

from ...helpers import check_type
from ._timestamp_schema import TimestampSchema

__all__ = ("TimestampSubstitutor",)


class TimestampSubstitutor(Substitutor, extend=True):
    def visit_timestamp(self, schema: TimestampSchema, *,
                        value: Any = Nil, **kwargs: Any) -> TimestampSchema:
        error = check_type(value, [str])
        if error:
            raise SubstitutionError(error)
        return schema.__class__(schema.props.update(value=value))
