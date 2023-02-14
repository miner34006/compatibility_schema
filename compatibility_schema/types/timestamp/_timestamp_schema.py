from typing import Any, Union

import delorean
from niltype import Nilable

from district42 import Props, SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42.errors import DeclarationError
from district42.types import Schema

from ...helpers import check_type

__all__ = ("TimestampSchema",)



class TimestampProps(Props):
    @property
    def value(self) -> Nilable[str]:
        return self.get("value")

    @property
    def iso(self) -> Nilable[bool]:
        return self.get("iso")

    @property
    def format(self) -> Nilable[str]:
        return self.get("format")



class TimestampSchema(Schema[TimestampProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_timestamp(self, **kwargs)

    def __call__(self, /, value: Union[str, delorean.Delorean]) -> "TimestampSchema":
        parsed_value = self.__parse_value(value)
        error = check_type(parsed_value, [str, delorean.Delorean])
        if error:
            raise DeclarationError(error)
        return self.__class__(self.props.update(value=parsed_value))

    def __parse_value(self, value: Union[str, delorean.Delorean]) -> delorean.Delorean:
        if isinstance(value, delorean.Delorean):
            return value
        try:
            return delorean.parse(value)
        except ValueError as e:
            raise DeclarationError(e)

    @property
    def iso(self) -> "TimestampSchema":
        return self.__class__(self.props.update(iso=True))

    def format(self, timestamp_format: str) -> "TimestampSchema":
        return self.__class__(self.props.update(format=timestamp_format))

    def min(self, value):
        raise NotImplementedError()

    def max(self, value):
        raise NotImplementedError()

    def between(self, min_value, max_value):
        raise NotImplementedError()

    @property
    def nullable(self):
        raise NotImplementedError()

