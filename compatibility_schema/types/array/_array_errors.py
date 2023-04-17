from typing import cast

from th import PathHolder
from valera import Formatter
from valera.errors import ValidationError

__all__ = ("ArrayFormatter",)


class ValidationExactlyOccurrenceError(ValidationError):
    def __init__(self, path: PathHolder, expected_schema, exactly_count) -> None:
        self.path = path
        self.expected_schema = expected_schema
        self.exactly_count = exactly_count

    def format(self, formatter: Formatter) -> str:
        return cast(str, formatter.format_array_exactly_occurrence_error(self))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path!r}, {self.expected_schema!r}, {self.exactly_count!r})"


class ValidationMinOccurrenceError(ValidationError):
    def __init__(self, path: PathHolder, expected_schema, min_count) -> None:
        self.path = path
        self.expected_schema = expected_schema
        self.min_count = min_count

    def format(self, formatter: Formatter) -> str:
        return cast(str, formatter.format_array_min_occurrence_error(self))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path!r}, {self.expected_schema!r}, {self.min_count!r})"


class ArrayFormatter(Formatter, extend=True):
    def format_array_exactly_occurrence_error(self, error: ValidationExactlyOccurrenceError) -> str:
        formatted_path = self._at_path(error.path)
        end = '' if error.exactly_count == 1 else 's'
        return f"Array{formatted_path} must contain exactly {error.exactly_count} "\
               f"occurrence{end} of {error.expected_schema}"

    def format_array_min_occurrence_error(self, error: ValidationExactlyOccurrenceError) -> str:
        formatted_path = self._at_path(error.path)
        end = '' if error.min_count == 1 else 's'
        return f"Array{formatted_path} must contain at least {error.min_count} "\
               f"occurrence{end} of {error.expected_schema}"
