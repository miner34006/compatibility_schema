import re
from typing import Any

from niltype import Nil, Nilable
from revolt import SubstitutorValidator
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import (AlphabetValidationError, LengthValidationError,
                           MaxLengthValidationError, MaxValueValidationError,
                           MinLengthValidationError, MinValueValidationError,
                           RegexValidationError, SubstrValidationError,
                           ValueValidationError)

from ._string_schema import StringSchema

__all__ = ("StringValidator", "StringSubstitutorValidator")


class StringValidator(Validator, extend=True):
    def __is_uri_valid(self, actual_val):
        from urllib.parse import urlparse
        attrs = urlparse(actual_val)
        return attrs.netloc or attrs.path

    def visit_string(self, schema: StringSchema, *,
                     value: Any = Nil, path: Nilable[PathHolder] = Nil,
                     **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, str):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        if schema.props.uri is not Nil:
            is_uri_valid = self.__is_uri_valid(value)
            if not is_uri_valid:
                return result.add_errors([ValueValidationError(path, value, 'uri string')])

        if schema.props.pattern is not Nil:
            match_object = re.search(schema.props.pattern, value)
            if match_object is None:
                error = RegexValidationError(path, value, schema.props.pattern)
                return result.add_error(error)

        if schema.props.min is not Nil:
            if int(value) < int(schema.props.min):
                result.add_error(MinValueValidationError(path, value, schema.props.min))

        if schema.props.max is not Nil:
            if int(value) > int(schema.props.max):
                result.add_error(MaxValueValidationError(path, value, schema.props.max))

        if schema.props.len is not Nil:
            if len(value) != schema.props.len:
                result.add_error(LengthValidationError(path, value, schema.props.len))
        if schema.props.min_len is not Nil:
            if len(value) < schema.props.min_len:
                result.add_error(MinLengthValidationError(path, value, schema.props.min_len))
        if schema.props.max_len is not Nil:
            if len(value) > schema.props.max_len:
                result.add_error(MaxLengthValidationError(path, value, schema.props.max_len))

        if schema.props.substr is not Nil:
            if schema.props.substr not in value:
                result.add_error(SubstrValidationError(path, value, schema.props.substr))

        if schema.props.alphabet is not Nil:
            alphabet = set(schema.props.alphabet)
            for letter in value:
                if letter not in alphabet:
                    return result.add_error(
                        AlphabetValidationError(PathHolder(), value, schema.props.alphabet))

        return result
