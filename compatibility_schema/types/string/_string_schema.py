import re
import string
from typing import Any, Union

from niltype import Nil, Nilable

from district42 import Props, SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42.errors import (DeclarationError, make_incorrect_len_error,
                               make_incorrect_max_len_error,
                               make_incorrect_min_len_error,
                               make_invalid_type_error)
from district42.types import Schema
from district42.utils import TypeOrEllipsis, is_ellipsis

__all__ = ("StringSchema",)



class StrProps(Props):
    @property
    def value(self) -> Nilable[str]:
        return self.get("value")

    @property
    def len(self) -> Nilable[int]:
        return self.get("len")

    @property
    def uri(self) -> Nilable[bool]:
        return self.get("uri")

    @property
    def min_len(self) -> Nilable[int]:
        return self.get("min_len")

    @property
    def max_len(self) -> Nilable[int]:
        return self.get("max_len")

    @property
    def alphabet(self) -> Nilable[str]:
        return self.get("alphabet")

    @property
    def substr(self) -> Nilable[str]:
        return self.get("substr")

    @property
    def pattern(self) -> Nilable[str]:
        return self.get("pattern")

    @property
    def min(self) -> Nilable[int]:
        return self.get("min")

    @property
    def max(self) -> Nilable[int]:
        return self.get("max")

    @property
    def numeric(self) -> Nilable[bool]:
        return self.get("numeric")


class StringSchema(Schema[StrProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_string(self, **kwargs)

    def __call__(self, /, value_or_numeric_min: Union[int, str], numeric_max: int = None) -> "StringSchema":
        if self.props.numeric:
            if not isinstance(value_or_numeric_min, int):
                raise make_invalid_type_error(self, value_or_numeric_min, (int,))
            if numeric_max and not isinstance(numeric_max, int):
                raise make_invalid_type_error(self, numeric_max, (int,))

            props = self.props.update(min=value_or_numeric_min)
            if numeric_max is not None:
                props = props.update(max=numeric_max)
            return self.__class__(props)

        if not isinstance(value_or_numeric_min, str):
            raise make_invalid_type_error(self, value_or_numeric_min, (str,))
        return self.__class__(self.props.update(value=value_or_numeric_min))

    def __declare_len(self, props: StrProps, length: Any) -> StrProps:
        if not isinstance(length, int):
            raise make_invalid_type_error(self, length, (int,))

        if (props.value is not Nil) and (len(props.value) != length):
            raise make_incorrect_len_error(self, props.value, length)

        return props.update(len=length)

    def __declare_min_len(self, props: StrProps, min_length: Any) -> StrProps:
        if not isinstance(min_length, int):
            raise make_invalid_type_error(self, min_length, (int,))

        if (props.value is not Nil) and (min_length > len(props.value)):
            raise make_incorrect_min_len_error(self, props.value, min_length)

        return props.update(min_len=min_length)

    def __declare_max_len(self, props: StrProps, max_length: Any) -> StrProps:
        if not isinstance(max_length, int):
            raise make_invalid_type_error(self, max_length, (int,))

        if (props.value is not Nil) and (max_length < len(props.value)):
            raise make_incorrect_max_len_error(self, props.value, max_length)

        return props.update(max_len=max_length)

    def __len(self, /, val_or_min: TypeOrEllipsis[int],
            max: Nilable[TypeOrEllipsis[int]] = Nil) -> "StringSchema":
        props = self.props
        if is_ellipsis(val_or_min):
            props = self.__declare_max_len(props, max)
        else:
            if max is Nil:
                props = self.__declare_len(props, val_or_min)
            elif is_ellipsis(max):
                props = self.__declare_min_len(props, val_or_min)
            else:
                props = self.__declare_max_len(self.__declare_min_len(props, val_or_min), max)
        return self.__class__(props)

    def __alphabet(self, /, letters: str) -> "StringSchema":
        if not isinstance(letters, str):
            raise make_invalid_type_error(self, letters, (str,))

        if self.props.value is not Nil:
            missing_letters = {x for x in self.props.value if x not in letters}
            if len(missing_letters) > 0:
                message = f"`{self!r}` alphabet is missing letters: "
                message += repr("".join(sorted(missing_letters)))
                raise DeclarationError(message)

        return self.__class__(self.props.update(alphabet=letters))

    def contains(self, substr: str) -> "StringSchema":
        if not isinstance(substr, str):
            raise make_invalid_type_error(self, substr, (str,))

        if self.props.value is not Nil:
            if substr not in self.props.value:
                message = f"`{self!r}` does not contain {substr!r}"
                raise DeclarationError(message)

        return self.__class__(self.props.update(substr=substr))

    def pattern(self, pattern: str, **kwargs) -> "StringSchema":
        if not isinstance(pattern, str):
            raise make_invalid_type_error(self, pattern, (str,))

        try:
            re.compile(pattern)
        except re.error as e:
            message = f"Invalid pattern ({e})"
            raise DeclarationError(message) from None

        if self.props.value is not Nil:
            if re.search(pattern, self.props.value) is None:
                message = f"`{self!r}` does not match {pattern!r}"
                raise DeclarationError(message)

        return self.__class__(self.props.update(pattern=pattern, **kwargs))

    @property
    def uri(self) -> "StringSchema":
        return self.__class__(self.props.update(uri=True))

    @property
    def alphabetic(self) -> "StringSchema":
        return self.__alphabet(string.ascii_letters)

    @property
    def numeric(self) -> "StringSchema":
        return self.pattern(r'^\-?[0-9]+$', numeric=True)

    @property
    def alpha_num(self) -> "StringSchema":
        return self.__alphabet(string.ascii_letters + string.digits)

    @property
    def lowercase(self) -> "StringSchema":
        return self.__alphabet(string.ascii_lowercase)

    @property
    def uppercase(self) -> "StringSchema":
        return self.__alphabet(string.ascii_uppercase)

    def length(self, *args) -> "StringSchema":
        if len(args) == 1:
            return self.__len(args[0], args[0])
        return self.__len(args[0], args[1])

    def min_length(self, value) -> "StringSchema":
        return self.__len(value, ...)

    def max_length(self, value) -> "StringSchema":
        return self.__len(..., value)

    @property
    def empty(self) -> "StringSchema":
        return self.__len(0)

    @property
    def non_empty(self) -> "StringSchema":
        return self.__len(1, ...)

    @property
    def nullable(self):
        raise NotImplementedError()
