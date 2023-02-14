from typing import Any

from niltype import Nil

from district42.representor import Representor

from ._string_schema import StringSchema

__all__ = ("StringRepresentor",)


class StringRepresentor(Representor, extend=True):
    def visit_string(self, schema: StringSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.string"

        if schema.props.numeric is not Nil:
            if (schema.props.min is not Nil) and (schema.props.max is not Nil):
                r += f".numeric({schema.props.min!r}, {schema.props.max!r})"
            elif schema.props.min is not Nil:
                r += f".numeric({schema.props.min!r})"
            else:
                r += f".numeric"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"

        if schema.props.alphabet is not Nil:
            r += f".alphabet({schema.props.alphabet!r})"

        if schema.props.substr is not Nil:
            r += f".contains({schema.props.substr!r})"

        if schema.props.pattern is not Nil and schema.props.numeric is Nil:
            r += f".pattern({schema.props.pattern!r})"
        elif schema.props.uri is not Nil:
            r += f".uri"

        if schema.props.len is not Nil:
            r += f".length({schema.props.len!r})"
        elif (schema.props.min_len is not Nil) and (schema.props.max_len is not Nil):
            r += f".length({schema.props.min_len!r}, {schema.props.max_len!r})"
        elif schema.props.min_len is not Nil:
            r += f".min_length({schema.props.min_len!r})"
        elif schema.props.max_len is not Nil:
            r += f".max_length({schema.props.max_len!r})"
        return r