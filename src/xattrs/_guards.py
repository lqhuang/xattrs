# SPDX-License-Identifier: MIT
from __future__ import annotations

from collections.abc import Sequence
from xattrs._compat.typing import (
    Annotated,
    Any,
    NewType,
    Optional,
    Type,
    TypedDict,
    TypeGuard,
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
