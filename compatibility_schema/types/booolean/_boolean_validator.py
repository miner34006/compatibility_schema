import re
from typing import Any

from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from revolt import SubstitutorValidator


from ._boolean_schema import BooleanSchema

__all__ = ("BooleanValidator",)


class BooleanValidator(Validator, extend=True):
    def visit_boolean(self, schema: BooleanSchema, *,
                     value: Any = Nil, path: Nilable[PathHolder] = Nil,
                     **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, bool):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        return result


class BooleanSubstitutorValidator(SubstitutorValidator, extend=True):
    def visit_boolean(self, schema: BooleanSchema, *,
                      value: Any = Nil, path: Nilable[PathHolder] = Nil,
                      **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, bool):
            return result.add_error(error)
        return result
