from datetime import datetime, timezone
from typing import Any

import delorean
from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import TypeValidationError, ValueValidationError

from ._timestamp_errors import TimestampFormatError, TimestampValidationError
from ._timestamp_schema import TimestampSchema

__all__ = ("TimestampValidator",)

iso8601 = r'^([\+-]?\d{4}(?!\d{2}\b))((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d|[12]\d{2}|3([0-5]\d|6[1-6])))([T\s]((([01]\d|2[0-3])((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?$'


class TimestampValidator(Validator, extend=True):
    def __is_type_valid(self, actual_val, valid_types):
        if type(actual_val) in valid_types:
            return True
        return False

    def __is_pattern_match(self, actual_val, pattern):
        import re
        return re.compile(pattern).match(actual_val)

    def visit_timestamp(self, schema: TimestampSchema, *,
                        value: Any = Nil, path: Nilable[PathHolder] = Nil,
                        **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        is_type_valid = self.__is_type_valid(value, [str, delorean.Delorean])
        if not is_type_valid:
            return result.add_error(TypeValidationError(path, value, [str, delorean.Delorean]))

        if schema.props.format is not Nil:
            try:
                dt = datetime.strptime(value, schema.props.format)
            except (TypeError, ValueError):
                return result.add_error(TimestampFormatError(path, value, schema.props.format))

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            timestamp = delorean.epoch(dt.timestamp())
        else:
            try:
                timestamp = delorean.parse(value)
            except (TypeError, ValueError):
                return result.add_error(TimestampValidationError(path, value))

        if schema.props.value is not Nil:
            expected_val = schema.props.value
            is_value_valid = (expected_val == timestamp)
            if not is_value_valid:
                return result.add_error(
                    ValueValidationError(path, value, expected_val.datetime.isoformat())
                )

        errors = []
        if schema.props.iso is not Nil:
            is_pattern_match = self.__is_pattern_match(value, iso8601)
            if not is_pattern_match:
                errors += [TimestampFormatError(path, value, 'ISO 8601')]
        elif schema.props.format is not Nil:
            expected_format = schema.props.format
            if value != timestamp.datetime.strftime(expected_format):
                errors += [TimestampFormatError(path, value, expected_format)]
        return result.add_errors(errors)
