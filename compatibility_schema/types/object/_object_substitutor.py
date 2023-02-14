from copy import deepcopy
from typing import Any

from district42 import from_native
from niltype import Nil
from revolt import Substitutor
from revolt.errors import SubstitutionError

from ...helpers import check_type, roll_out
from ._object_schema import ObjectProps, ObjectSchema

__all__ = ("ObjectSubstitutor",)


class ObjectSubstitutor(Substitutor, extend=True):
    def visit_object(self, schema: ObjectSchema, *,
                     value: Any = Nil, **kwargs: Any) -> ObjectSchema:
        error = check_type(value, [dict])
        if error:
            raise SubstitutionError(error)

        rolled_keys = roll_out(value)
        if schema.props.keys is not Nil:
            clone = ObjectSchema(deepcopy(schema.props))

            for key, value in clone.props.keys.items():
                if key not in rolled_keys: continue
                is_required = value[1]
                if not is_required:
                    clone.props.keys[key] = value[0], True
                new_value = clone.props.keys[key][0] % rolled_keys[key]
                clone.props.keys[key] = (new_value, clone.props.keys[key][1])

            v = clone.strict if schema.props.strict is not Nil else clone
            return v

        object_keys = {}
        for key, val in rolled_keys.items():
            object_keys[key] = (from_native(val), True)

        substituted = schema.__class__(schema.props.update(keys=object_keys))
        return substituted.strict if (schema.props.strict is not Nil) else substituted
