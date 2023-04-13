from copy import deepcopy
from typing import Any

from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import (LengthValidationError, MaxLengthValidationError,
                           MinLengthValidationError,
                           MissingElementValidationError, TypeValidationError)

from ._array_errors import (ValidationExactlyOccurrenceError,
                            ValidationMinOccurrenceError)
from ._array_schema import ArraySchema

__all__ = ("ArrayValidator", )


class ArrayValidator(Validator, extend=True):
    def __count_occurrences(self, schema, value):
        count = 0
        for _, item in enumerate(value):
            res = schema.__accept__(self, value=item)
            if len(res.get_errors()) == 0:
                count += 1
        return count

    def __is_length_match(self, actual_val, expected_length, comparator):
        return getattr(len(actual_val), comparator)(expected_length)

    def __is_type_valid(self, actual_val, valid_types):
        if type(actual_val) in valid_types:
            return True
        return False

    def visit_array(self, schema: ArraySchema, *,
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
        if schema.props.items is not Nil:
            for index, item in enumerate(schema.props.items):
                try:
                    new_value = value[index]
                    nested_path = deepcopy(path)[index]
                    errors += item.__accept__(self, path=nested_path, value=new_value, **kwargs).get_errors()
                except IndexError:
                    errors.append(MissingElementValidationError(path, value, index))

            expected_length = len(schema.props.items)
            if not self.__is_length_match(value, expected_length, '__le__'):
                errors.append(LengthValidationError(path, value, expected_length))

        elif schema.props.contains is not Nil:
            count = self.__count_occurrences(schema.props.contains, value)
            if count == 0:
                errors.append(ValidationMinOccurrenceError(path, schema.props.contains, 1))
        elif schema.props.contains_one is not Nil:
            count = self.__count_occurrences(schema.props.contains_one, value)
            if count != 1:
                errors.append(ValidationExactlyOccurrenceError(path, schema.props.contains_one, 1))
        elif schema.props.contains_many is not Nil:
            count = self.__count_occurrences(schema.props.contains_many, value)
            if count < 2:
                errors.append(ValidationMinOccurrenceError(path, schema.props.contains_many, 2))
        elif schema.props.contains_all is not Nil:
            for item in schema.props.contains_all:
                count = self.__count_occurrences(item, value)
                if count == 0:
                    errors.append(ValidationMinOccurrenceError(path, item, 1))

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
