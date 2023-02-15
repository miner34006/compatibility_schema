from typing import List, Union, Any

from niltype import Nilable

from district42 import Props, SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42 import GenericSchema, Schema
from district42.errors import DeclarationError, make_invalid_type_error
from district42.types._list_schema import ElementType


class ArrayOfProps(Props):
    @property
    def type(self) -> Nilable[Schema]:
        return self.get("type")

    @property
    def length(self) -> Nilable[int]:
        return self.get("length")

    @property
    def empty(self) -> Nilable[bool]:
        return self.get("empty")

    @property
    def min_length(self) -> Nilable[int]:
        return self.get("min_length")

    @property
    def max_length(self) -> Nilable[int]:
        return self.get("max_length")


class ArrayOfSchema(Schema[ArrayOfProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_array_of(self, **kwargs)

    def __call__(self, /,
                 elements_or_type: Union[List[ElementType], GenericSchema]) -> "ArrayOfSchema":
        if not isinstance(elements_or_type, (Schema)):
            raise make_invalid_type_error(self, elements_or_type, (Schema))
        return self.__class__(self.props.update(type=elements_or_type))

    def length(self, *args) -> "ArrayOfSchema":
        if not (1 <= len(args) <= 2):
            raise DeclarationError()
        if len(args) == 1:
            return self.__class__(self.props.update(length=args[0]))
        return self.__class__(self.props.update(min_length=args[0], max_length=args[1]))

    def min_length(self, value: int) -> "ArrayOfSchema":
        return self.__class__(self.props.update(min_length=value))

    def max_length(self, value: int) -> "ArrayOfSchema":
        return self.__class__(self.props.update(max_length=value))

    @property
    def empty(self) -> "ArrayOfSchema":
        return self.__class__(self.props.update(empty=True, length=0))

    @property
    def non_empty(self) -> "ArrayOfSchema":
        return self.__class__(self.props.update(empty=False, min_length=1))

    @property
    def unique(self):
        raise NotImplementedError()

    @property
    def nullable(self):
        raise NotImplementedError()
