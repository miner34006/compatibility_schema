from copy import deepcopy
from typing import Any

from niltype import Nil, Nilable

from district42 import Props, SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42.errors import DeclarationError
from district42.types import Schema

from ...helpers import check_type, roll_out

__all__ = ("ObjectSchema",)


class ObjectProps(Props):
    @property
    def keys(self) -> Nilable[dict]:
        return self.get("keys")

    @property
    def length(self) -> Nilable[int]:
        return self.get("length")

    @property
    def max_length(self) -> Nilable[int]:
        return self.get("max_length")

    @property
    def min_length(self) -> Nilable[int]:
        return self.get("min_length")

    @property
    def empty(self) -> Nilable[bool]:
        return self.get("empty")

    @property
    def strict(self) -> Nilable[bool]:
        return self.get("strict")


class ObjectSchema(Schema[ObjectProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_object(self, **kwargs)

    def __call__(self, keys: dict) -> "ObjectSchema":
        error = check_type(keys, [dict])
        if error:
            raise DeclarationError(error)
        return self.__class__(self.props.update(keys=self.__roll_out(keys)))

    def __contains__(self, composite_key: str) -> bool:
        parts = composite_key.split('.')
        if len(parts) == 1:
            return parts[0] in self.props.keys
        return parts[0] in self.props.keys and '.'.join(parts[1:]) in self.props.keys[parts[0]]

    def __getitem__(self, composite_key: str) -> Schema:
        parts = composite_key.split('.')
        if len(parts) == 1:
            return self.props.keys[parts[0]][0]
        return self.props.keys[parts[0]]['.'.join(parts[1:])]

    def __add__(self, keys) -> "ObjectSchema":
        error = check_type(keys, [Schema, dict])
        if error:
            raise DeclarationError(error)
        clone = deepcopy(self)
        clone.props.keys.update(self.__roll_out(keys))
        return clone

    def __rename_keys(self, keys: dict, new_keys: dict) -> dict:
        renamed = {}
        for key, val in keys.items():
            new_key = new_keys.get(key, key)
            if isinstance(new_key, dict):
                renamed[key] = val[0].__matmul__(new_key)
            else:
                renamed[new_key] = val
        return renamed

    def __matmul__(self, other: dict) -> "ObjectSchema":
        if self.props.keys is not Nil:
            new_keys = self.__rename_keys(self.props.keys, roll_out(other))
            return self.__class__(self.props.update(keys=new_keys))
        return self.__class__(self.props)

    def items(self) -> list:
        return self.props.keys.items()

    def __roll_out(self, keys):
        new_keys = {}
        for composite_key, val in keys.items():
            if isinstance(val, tuple):
                val = val[0]
            error = check_type(val, [Schema])
            if error:
                raise DeclarationError(error)
            is_required = True
            parts = composite_key.split('.')
            key = parts[0]
            if key[-1] == '?':
                key = key[:-1]
                is_required = False
            if len(parts) == 1:
                new_keys[key] = (deepcopy(val), is_required)
            else:
                comp_key = '.'.join(parts[1:])
                if key not in new_keys:
                    new_keys[key] = (self.__class__()({comp_key: val}), is_required)
                else:
                    new_keys[key].props.keys.update(self.__roll_out({comp_key: val}))
        return new_keys

    @property
    def strict(self) -> "ObjectSchema":
        return self.__class__(self.props.update(strict=True))

    def length(self, *args) -> "ObjectSchema":
        if not (1 <= len(args) <= 2):
            raise DeclarationError()

        if len(args) == 1:
            return self.__class__(self.props.update(length=args[0]))

        return self.__class__(self.props.update(
            min_length=args[0],
            max_length=args[1]
        ))

    def min_length(self, value: int) -> "ObjectSchema":
        return self.__class__(self.props.update(min_length=value))

    def max_length(self, value: int) -> "ObjectSchema":
        return self.__class__(self.props.update(max_length=value))

    @property
    def empty(self) -> "ObjectSchema":
        return self.__class__(self.props.update(
            empty=True,
            length=0
        ))

    @property
    def non_empty(self) -> "ObjectSchema":
        return self.__class__(self.props.update(
            empty=False,
            min_length=1
        ))

    @property
    def nullable(self):
        raise NotImplementedError()
