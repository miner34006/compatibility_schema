from typing import Any

from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import (LengthValidationError, MaxLengthValidationError,
                           MinLengthValidationError, TypeValidationError)

from ._array_of_schema import ArrayOfSchema

__all__ = ("ArrayOfValidator", )


class ArrayOfValidator(Validator, extend=True):
    def __is_type_valid(self, actual_val, valid_types):
        if type(actual_val) in valid_types:
            return True
        return False

    def __is_length_match(self, actual_val, expected_length, comparator):
        return getattr(len(actual_val), comparator)(expected_length)

    def visit_array_of(self, schema: ArrayOfSchema, *,
                       value: Any = Nil, path: Nilable[PathHolder] = Nil,
                       **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        valid_types = [list]
        is_type_valid = self.__is_type_valid(value, valid_types)
        if not is_type_valid:
            return result.add_error(TypeValidationError(path, value, list))

        errors = []
        for index, item in enumerate(value):
            errors += (schema.props.type.__accept__(self, value=item)).get_errors()

        if schema.props.length is not Nil:
            if not self.__is_length_match(value, schema.props.length, '__eq__'):
                errors.append(LengthValidationError(path, value, schema.props.length))
        if schema.props.min_length is not Nil:
            if not self.__is_length_match(value, schema.props.min_length, '__ge__'):
                errors.append(MinLengthValidationError(path, value, schema.props.min_length))
        if schema.props.max_length is not Nil:
            if not self.__is_length_match(value, schema.props.max_length, '__le__'):
                errors.append(MaxLengthValidationError(path, value, schema.props.max_length))
        return result.add_errors(errors)
