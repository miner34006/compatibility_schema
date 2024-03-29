from copy import deepcopy
from typing import Any

from niltype import Nil, Nilable
from revolt import SubstitutorValidator
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import (ExtraKeyValidationError, LengthValidationError,
                           MaxLengthValidationError, MinLengthValidationError,
                           MissingKeyValidationError, TypeValidationError)

from ._object_schema import ObjectSchema

__all__ = ("ObjectValidator", "ObjectSubstitutorValidator")


def is_length_match(actual_val, expected_length, comparator):
    return getattr(len(actual_val), comparator)(expected_length)


def is_type_valid(actual_val, valid_types):
    if type(actual_val) in valid_types:
        return True
    return False


class ObjectValidator(Validator, extend=True):
    def visit_object(self, schema: ObjectSchema, *,
                     value: Any = Nil, path: Nilable[PathHolder] = Nil,
                     **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        valid_types = [dict]
        if not is_type_valid(value, valid_types):
            return result.add_errors([TypeValidationError(path, value, dict)])

        errors = []
        if schema.props.keys is not Nil:
            for key, val in schema.props.keys.items():
                nested_path = deepcopy(path)[key]
                try:
                    res = val[0].__accept__(self, value=value[key], path=nested_path, **kwargs)
                    errors.extend(res.get_errors())
                except KeyError:
                    is_required = val[1]
                    if is_required:
                        errors += [MissingKeyValidationError(path, val, key)]

        if (schema.props.keys is not Nil) and (schema.props.strict is not Nil):
            for key in value.keys():
                if key not in schema.props.keys:
                    errors += [ExtraKeyValidationError(path, None, key)]

        if schema.props.length is not Nil:
            if not is_length_match(value, schema.props.length, '__eq__'):
                errors += [LengthValidationError(path, value, schema.props.length)]
        if schema.props.min_length is not Nil:
            if not is_length_match(value, schema.props.min_length, '__ge__'):
                errors += [MinLengthValidationError(path, value, schema.props.min_length)]
        if schema.props.max_length is not Nil:
            if not is_length_match(value, schema.props.max_length, '__le__'):
                errors += [MaxLengthValidationError(path, value, schema.props.max_length)]

        return result.add_errors(errors)


class ObjectSubstitutorValidator(SubstitutorValidator, extend=True):
    def visit_object(self, schema: ObjectSchema, *,
                     value: Any = Nil, path: Nilable[PathHolder] = Nil,
                     **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        valid_types = [dict]
        if not is_type_valid(value, valid_types):
            return result.add_errors([TypeValidationError(path, value, dict)])

        errors = []
        if schema.props.keys is not Nil:
            for key, val in schema.props.keys.items():
                nested_path = deepcopy(path)[key]
                try:
                    res = val[0].__accept__(self, value=value[key], path=nested_path, **kwargs)
                    errors.extend(res.get_errors())
                except KeyError:
                    pass

        if (schema.props.keys is not Nil) and (schema.props.strict is not Nil):
            for key in value.keys():
                if key not in schema.props.keys:
                    errors += [ExtraKeyValidationError(path, None, key)]

        if schema.props.length is not Nil:
            if not is_length_match(value, schema.props.length, '__eq__'):
                errors += [LengthValidationError(path, value, schema.props.length)]
        if schema.props.min_length is not Nil:
            if not is_length_match(value, schema.props.min_length, '__ge__'):
                errors += [MinLengthValidationError(path, value, schema.props.min_length)]
        if schema.props.max_length is not Nil:
            if not is_length_match(value, schema.props.max_length, '__le__'):
                errors += [MaxLengthValidationError(path, value, schema.props.max_length)]

        return result.add_errors(errors)
