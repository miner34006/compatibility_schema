from district42 import from_native
from district42.types import AnySchema


class EnumSchema(AnySchema):
    def __call__(self, enumerator1, enumerator2, *enumerators) -> "EnumSchema":
        all_enumerators = [enumerator1, enumerator2] + list(enumerators)
        types = [from_native(x) for x in all_enumerators]
        return super().__call__(*types)

    @property
    def nullable(self):
        raise NotImplementedError()
