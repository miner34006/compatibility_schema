from typing import Any

from niltype import  Nilable

from district42 import Props, SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42.errors import make_invalid_type_error
from district42.types import Schema

__all__ = ("StringSchema",)


class BooleanProps(Props):
    @property
    def value(self) -> Nilable[bool]:
        return self.get("value")


class BooleanSchema(Schema[BooleanProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_boolean(self, **kwargs)

    def __call__(self, /, value: bool) -> "BooleanSchema":
        if not isinstance(value, int):
            raise make_invalid_type_error(self, value, (bool,))
        return self.__class__(self.props.update(value=value))

    def nullable(self):
        raise NotImplementedError()
