from typing import Any

from blahblah import Generator
from blahblah._consts import (INT_MAX, INT_MIN, STR_ALPHABET, STR_LEN_MAX,
                              STR_LEN_MIN)
from niltype import Nil

from ._string_schema import StringSchema

__all__ = ("StringGenerator",)


class StringGenerator(Generator, extend=True):
    def visit_string(self, schema: StringSchema, **kwargs: Any) -> str:
        if schema.props.value is not Nil:
            return schema.props.value

        if schema.props.uri is not Nil:
            return 'http://localhost/'

        if schema.props.numeric is not Nil:
            min_value = INT_MIN
            if schema.props.min is not Nil:
                min_value = int(schema.props.min)

            max_value = INT_MAX
            if schema.props.max is not Nil:
                max_value = int(schema.props.max)

            return str(self._random.random_int(min_value, max_value))

        if schema.props.pattern is not Nil:
            return self._regex_generator.generate(schema.props.pattern)

        if schema.props.len is not Nil:
            length = schema.props.len
        else:
            min_length = schema.props.min_len if (schema.props.min_len is not Nil) else STR_LEN_MIN
            max_length = schema.props.max_len if (schema.props.max_len is not Nil) else STR_LEN_MAX
            if schema.props.substr is not Nil:
                min_length = max(min_length, len(schema.props.substr))
                max_length = max(max_length, len(schema.props.substr))
            length = self._random.random_int(min_length, max_length)

        if schema.props.alphabet is not Nil:
            alphabet = schema.props.alphabet
        else:
            alphabet = STR_ALPHABET

        if schema.props.substr is not Nil:
            substr = schema.props.substr
            generated = self._random.random_str(length - len(substr), alphabet)
            offset = self._random.random_int(0, len(generated))
            return generated[0:offset] + substr + generated[offset:]

        return self._random.random_str(length, alphabet)
