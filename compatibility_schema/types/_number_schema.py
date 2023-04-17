from typing import Any, Union

from district42 import Schema, SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42._props import Props
from district42.errors import (make_incorrect_max_error,
                               make_incorrect_min_error,
                               make_invalid_type_error)
from niltype import Nil, Nilable

__all__ = ("NumberSchema", "NumberProps",)


class NumberProps(Props):
    @property
    def value(self) -> Nilable[int]:
        return self.get("value")

    @property
    def min(self) -> Nilable[int]:
        return self.get("min")

    @property
    def max(self) -> Nilable[int]:
        return self.get("max")

    @property
    def is_float(self) -> Nilable[bool]:
        return self.get("is_float")


class NumberSchema(Schema[NumberProps]):
    def __check_types(self, value: Union[int, float]):
        if not self.props.is_float and not isinstance(value, int):
            raise make_invalid_type_error(self, value, (int,))

        if self.props.is_float and not isinstance(value, float):
            raise make_invalid_type_error(self, value, (float,))

    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        if self.props.is_float:
            return visitor.visit_float(self, **kwargs)
        return visitor.visit_int(self, **kwargs)

    def __call__(self, /, value: Union[int, float]) -> "NumberSchema":
        self.__check_types(value)
        return self.__class__(self.props.update(value=value))

    def min(self, /, value: Union[int, float]) -> "NumberSchema":
        self.__check_types(value)
        if (self.props.value is not Nil) and (value > self.props.value):
            raise make_incorrect_min_error(self, self.props.value, value)

        return self.__class__(self.props.update(min=value))

    def max(self, /, value: Union[int, float]) -> "NumberSchema":
        self.__check_types(value)
        if (self.props.value is not Nil) and (value < self.props.value):
            raise make_incorrect_max_error(self, self.props.value, value)

        return self.__class__(self.props.update(max=value))

    @property
    def integer(self):
        return self.__class__(self.props.update(is_float=False))

    @property
    def float(self):
        return self.__class__(self.props.update(is_float=True))

    @property
    def positive(self):
        min_value = 1.0 if self.props.is_float else 1
        return self.__class__(self.props.update(min=min_value))

    @property
    def non_positive(self):
        max_value = 0.0 if self.props.is_float else 0
        return self.__class__(self.props.update(max=max_value))

    @property
    def negative(self):
        max_value = -1.0 if self.props.is_float else -1
        return self.__class__(self.props.update(max=max_value))

    @property
    def non_negative(self):
        min_value = 0.0 if self.props.is_float else 0
        return self.__class__(self.props.update(min=min_value))

    @property
    def zero(self):
        value = 0.0 if self.props.is_float else 0
        return self.__class__(self.props.update(value=value))

    def between(self, min_value, max_value):
        return self.__class__(self.props.update(min=min_value, max=max_value))

    @property
    def unsigned(self):
        raise NotImplementedError()

    def multiple(self, base):
        raise NotImplementedError()

    def precision(self, places):
        raise NotImplementedError()

    @property
    def nullable(self):
        raise NotImplementedError()
