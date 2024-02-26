# SPDX-License-Identifier: BSD-3-Clause

from collections.abc import Sequence
from xattrs._compat.typing import Annotated, Any, Optional, Type, TypedDict, TypeGuard
from xattrs._compat.typing import is_typeddict as _is_typeddict

from dataclasses import is_dataclass as _is_dataclass


def is_optional(typ: Type) -> TypeGuard[Optional[Any]]: ...


def is_annotated(typ: Any) -> TypeGuard[Annotated]: ...


def is_sequence(typ: Any) -> TypeGuard[Sequence]: ...


def is_hetero_sequence(typ: Any) -> TypeGuard[Sequence]: ...


def is_tuple(typ: Any) -> TypeGuard[tuple]: ...


def is_hetero_tuple(typ: Any) -> TypeGuard[tuple]: ...


def is_typeddict(typ: Any) -> TypeGuard[TypedDict]: ...


def is_dataclass(typ: Any) -> TypeGuard[Annotated]: ...


def is_dataclass_transform(typ: Any) -> TypeGuard[Annotated]: ...
