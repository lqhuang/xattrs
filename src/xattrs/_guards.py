# SPDX-License-Identifier: BSD-3-Clause
from collections.abc import Sequence
from xattrs._compat.typing import (
    Annotated,
    Any,
    Optional,
    Type,
    TypedDict,
    TypeGuard,
    NewType,
)

from collections import defaultdict
from enum import Enum

from xattrs._types import _ATOMIC_TYPES


def is_atomic(typ: Any) -> bool:
    return type(typ) in _ATOMIC_TYPES


def is_optional(typ: Type) -> TypeGuard[Optional[Any]]: ...


def is_annotated(typ: Any) -> TypeGuard[Annotated]: ...


def is_sequence(typ: Any) -> TypeGuard[Sequence]: ...


def is_hetero_sequence(typ: Any) -> TypeGuard[Sequence]: ...


def is_tuple(typ: Any) -> TypeGuard[tuple]: ...


def is_hetero_tuple(typ: Any) -> TypeGuard[tuple]: ...


def is_typeddict(typ: Any): ...


def is_defaultdict(typ: Any) -> TypeGuard[dict]: ...


def is_dataclass_transform(typ: Any) -> TypeGuard[Annotated]: ...


def is_enum(typ: Any) -> TypeGuard[Enum]:
    try:
        return issubclass(typ, Enum)
    except TypeError:
        return isinstance(typ, Enum)


def is_new_type(type: Any) -> TypeGuard[NewType]: ...
