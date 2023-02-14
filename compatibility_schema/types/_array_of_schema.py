from typing import List, Union

from niltype import Nil, Nilable

from district42 import GenericSchema, Schema
from district42.errors import DeclarationError, make_invalid_type_error
from district42.types import ListSchema
from district42.types._list_schema import ElementType
from district42.utils import TypeOrEllipsis, is_ellipsis


class ArrayOfSchema(ListSchema):
    def __call__(self, /,
                 elements_or_type: Union[List[ElementType], GenericSchema]) -> "ArrayOfSchema":
        if not isinstance(elements_or_type, (list, Schema)):
            raise make_invalid_type_error(self, elements_or_type, (list, Schema))

        if isinstance(elements_or_type, Schema):
            return self.__class__(self.props.update(type=elements_or_type))

        for index, element in enumerate(elements_or_type):
            if not isinstance(element, (Schema, type(...))):
                raise make_invalid_type_error(self, element, (Schema, type(...)))
            if is_ellipsis(element):
                if (index != 0) and (index != len(elements_or_type) - 1):
                    raise DeclarationError("`...` must be first or last element")

        if len(elements_or_type) == 2 and \
           is_ellipsis(elements_or_type[0]) and is_ellipsis(elements_or_type[-1]):
            raise DeclarationError("`...` must be first or last element")

        return self.__class__(self.props.update(elements=elements_or_type))

    def __len(self, /, val_or_min: TypeOrEllipsis[int],
            max: Nilable[TypeOrEllipsis[int]] = Nil) -> "ArrayOfSchema":
        props = self.props
        if is_ellipsis(val_or_min):
            props = self._ListSchema__declare_max_len(props, max)
        else:
            if max is Nil:
                props = self._ListSchema__declare_len(props, val_or_min)
            elif is_ellipsis(max):
                props = self._ListSchema__declare_min_len(props, val_or_min)
            else:
                props = self._ListSchema__declare_max_len(
                    self._ListSchema__declare_min_len(props, val_or_min), max)
        return self.__class__(props)

    def length(self, *args) -> "ArrayOfSchema":
        if not (1 <= len(args) <= 2):
            raise DeclarationError()

        if len(args) == 1:
            return self.__len(args[0], args[0])
        else:
            return self.__len(args[0], args[1])

    def min_length(self, value: int) -> "ArrayOfSchema":
        return self.__len(value, ...)

    def max_length(self, value: int) -> "ArrayOfSchema":
        return self.__len(..., value)

    @property
    def empty(self) -> "ArrayOfSchema":
        return self.__len(0)

    @property
    def non_empty(self) -> "ArrayOfSchema":
        return self.__len(1, ...)

    @property
    def unique(self):
        raise NotImplementedError()

    @property
    def nullable(self):
        raise NotImplementedError()
