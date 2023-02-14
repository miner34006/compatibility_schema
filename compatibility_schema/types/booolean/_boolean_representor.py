from typing import Any

from niltype import Nil

from district42.representor import Representor

from ._boolean_schema import BooleanSchema

__all__ = ("BooleanRepresentor",)


class BooleanRepresentor(Representor, extend=True):
    def visit_boolean(self, schema: BooleanSchema, *, indent: int = 0, **kwargs: Any) -> str:
        r = f"{self._name}.boolean"

        if schema.props.value is not Nil:
            r += f"({schema.props.value!r})"
        return r