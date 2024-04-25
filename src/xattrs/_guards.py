# SPDX-License-Identifier: BSD-3-Clause

from collections.abc import Sequence
from xattrs._compat.typing import Annotated, Any, Optional, Type, TypedDict, TypeGuard

from dataclasses import is_dataclass  # TypeGuard is defined in mypy level


def is_optional(typ: Type) -> TypeGuard[Optional[Any]]: ...


def is_annotated(typ: Any) -> TypeGuard[Annotated]: ...


def is_sequence(typ: Any) -> TypeGuard[Sequence]: ...


def is_hetero_sequence(typ: Any) -> TypeGuard[Sequence]: ...


def is_tuple(typ: Any) -> TypeGuard[tuple]: ...


def is_hetero_tuple(typ: Any) -> TypeGuard[tuple]: ...


def is_typeddict(typ: Any): ...


def is_dataclass_transform(typ: Any) -> TypeGuard[Annotated]: ...
