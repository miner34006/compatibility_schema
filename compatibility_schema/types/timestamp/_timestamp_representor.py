from typing import Any

from district42.representor import Representor
from niltype import Nil

from ._timestamp_schema import TimestampSchema

__all__ = ("TimestampRepresentor",)


class TimestampRepresentor(Representor, extend=True):
    def __to_iso_format(self, timestamp):
        return timestamp.datetime.isoformat()

    def visit_timestamp(self, schema: TimestampSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.timestamp"

        if schema.props.value is not Nil:
            r += '({})'.format(repr(self.__to_iso_format(schema.props.value)))

        if schema.props.iso is not Nil:
            r += '.iso'
        elif schema.props.format is not Nil:
            r += '.format({})'.format(repr(schema.props.format))

        return r
