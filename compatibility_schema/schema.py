import warnings
from district42.types import AnySchema, BoolSchema, NoneSchema

from .types import (ArrayOfSchema, ArraySchema, EnumSchema, NumberSchema,
                    ObjectSchema, StringSchema, TimestampSchema)


class Schema:
    def ref(self, schema):
        return schema

    @property
    def null(self):
        return NoneSchema()

    @property
    def boolean(self):
        return BoolSchema()

    @property
    def number(self):
        raise NotImplementedError()

    @property
    def integer(self):
        return NumberSchema().integer

    @property
    def float(self):
        return NumberSchema().float

    @property
    def string(self):
        return StringSchema()

    @property
    def timestamp(self):
        return TimestampSchema()

    @property
    def array(self):
        return ArraySchema()

    @property
    def array_of(self):
        message = 'schema.array_of is deprecated, use schema.array.of instead'
        warnings.warn(message, DeprecationWarning, stacklevel=2)
        return ArrayOfSchema()

    @property
    def object(self):
        return ObjectSchema()

    @property
    def any(self):
        return AnySchema()

    @property
    def any_of(self):
        return AnySchema()

    @property
    def one_of(self):
        return AnySchema()

    @property
    def enum(self):
        return EnumSchema()

    @property
    def undefined(self):
        raise NotImplementedError()
