import random
from datetime import datetime
from time import time
from typing import Any

from blahblah import Generator
from niltype import Nil

from ._timestamp_schema import TimestampSchema

__all__ = ("TimestampGenerator",)


class TimestampGenerator(Generator, extend=True):
    def visit_timestamp(self, schema: TimestampSchema, **kwargs: Any) -> str:
        min_value, max_value = 0, int(time())
        if schema.props.value is not Nil:
            timestamp = datetime.utcfromtimestamp(schema.props.value.epoch())
        else:
            timestamp = datetime.utcfromtimestamp(random.randint(min_value, max_value))

        if schema.props.iso is not Nil:
            return timestamp.isoformat()

        if schema.props.format is not Nil:
            return timestamp.strftime(schema.props.format)

        return str(timestamp)
