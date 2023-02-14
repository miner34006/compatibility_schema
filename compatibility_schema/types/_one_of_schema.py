from district42.types import AnySchema


class OneofSchema(AnySchema):
    @property
    def nullable(self):
        raise NotImplementedError()
