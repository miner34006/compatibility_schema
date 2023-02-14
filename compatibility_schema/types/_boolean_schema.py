from district42.types import BoolSchema


class BooleanSchema(BoolSchema):
    @property
    def nullable(self):
        raise NotImplementedError()
