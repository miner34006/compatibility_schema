from typing import Any, cast

from th import PathHolder
from valera import Formatter
from valera.errors import ValidationError

__all__ = ("TimestampFormatter",)


class TimestampValidationError(ValidationError):
    def __init__(self, path: PathHolder, value: Any) -> None:
        self.path = path
        self.value = value

    def format(self, formatter: Formatter) -> str:
        return cast(str, formatter.format_timestamp_error(self))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path!r}, {self.value!r})"


class TimestampFormatError(ValidationError):
    def __init__(self, path: PathHolder, value: Any, format_value: str) -> None:
        self.path = path
        self.value = value
        self.format_value = format_value

    def format(self, formatter: Formatter) -> str:
        return cast(str, formatter.format_timestamp_format_error(self))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path!r}, {self.value!r}, {self.format_value!r})"


class TimestampFormatter(Formatter, extend=True):
    def format_timestamp_error(self, error: TimestampValidationError) -> str:
        formatted_path = self._at_path(error.path)
        return f"Value{formatted_path} must be a valid string representation of a timestamp"

    def format_timestamp_format_error(self, error):
        formatted_path = self._at_path(error.path)
        return (f"Value{formatted_path} "
                f"must match format {error.format_value!r}, but {error.value!r} given")
