from district42.types import AnySchema


class AnySchema(AnySchema):
    @property
    def nullable(self):
        raise NotImplementedError()

