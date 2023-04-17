from typing import Any, List, Union

from district42 import Props, SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42.errors import DeclarationError
from district42.types import Schema
from niltype import Nilable

from ...helpers import check_type, check_types


class ArrayProps(Props):
    @property
    def items(self) -> Nilable[Schema]:
        return self.get("items")

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

    @property
    def contains(self) -> Nilable[Schema]:
        return self.get("contains")

    @property
    def contains_one(self) -> Nilable[Schema]:
        return self.get("contains_one")

    @property
    def contains_many(self) -> Nilable[Schema]:
        return self.get("contains_many")

    @property
    def contains_all(self) -> Nilable[List[Schema]]:
        return self.get("contains_all")


class ArraySchema(Schema[ArrayProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_array(self, **kwargs)

    def __call__(self, items: Union[list, Schema]) -> "ArraySchema":
        error = check_type(items, [list]) or check_types(items, [Schema])
        if error:
            raise DeclarationError(error)
        return self.__class__(self.props.update(items=items))

    @property
    def of(self):
        from .. import ArrayOfSchema
        return ArrayOfSchema()

    def contains(self, item) -> "ArraySchema":
        error = check_type(item, [Schema])
        if error:
            raise DeclarationError(error)
        return self.__class__(self.props.update(contains=item))

    def contains_one(self, item) -> "ArraySchema":
        error = check_type(item, [Schema])
        if error:
            raise DeclarationError(error)
        return self.__class__(self.props.update(contains_one=item))

    def contains_many(self, item) -> "ArraySchema":
        error = check_type(item, [Schema])
        if error:
            raise DeclarationError(error)
        return self.__class__(self.props.update(contains_many=item))

    def contains_all(self, items: List[Schema]) -> "ArraySchema":
        error = check_types(items, [Schema])
        if error:
            raise DeclarationError(error)
        return self.__class__(self.props.update(contains_all=list(items)))

    @property
    def empty(self) -> "ArraySchema":
        return self.__class__(self.props.update(empty=True, length=0))

    @property
    def non_empty(self) -> "ArraySchema":
        return self.__class__(self.props.update(empty=False, min_length=1))

    def length(self, *args) -> "ArraySchema":
        if not (1 <= len(args) <= 2):
            raise DeclarationError()
        if len(args) == 1:
            return self.__class__(self.props.update(length=args[0]))
        return self.__class__(self.props.update(min_length=args[0], max_length=args[1]))

    def min_length(self, value: int) -> "ArraySchema":
        return self.__class__(self.props.update(min_length=value))

    def max_length(self, value: int) -> "ArraySchema":
        return self.__class__(self.props.update(max_length=value))

    @property
    def unique(self):
        raise NotImplementedError()

    @property
    def nullable(self):
        raise NotImplementedError()
