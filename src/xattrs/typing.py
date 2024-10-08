# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Hashable,
    Literal,
    Protocol,
)
from xattrs._typing import T, T_co, T_contra

from dataclasses import Field

from attrs import Attribute

StructAs = Literal["dict", "tuple"]

# easy to remember?
CaseConvention = Literal[
    "lowercase",
    "UPPERCASE",
    "uppercase",
    "Capitalcase",
    "capitalcase",
    "snake_case",
    "kebab-case",
    "CONST_CASE",
    "camelCase",
    "PascalCase",
    # "Ada_Case", # NotImplemented
    # "COBOL-CASE", # NotImplemented
    # "Train-Case", # NotImplemented
]
CaseConverter = Callable[[str], str]
KeyConverter = Callable[[str], str]

FilterBuiltins = Literal[
    "exclude_if_default",
    "exclude_if_none",
    "exclude_if_false",
]
if TYPE_CHECKING:
    FilterCallable = (
        Callable[[Attribute[T], T], bool]
        | Callable[[Field[T], T], bool]
        | Callable[[Hashable, T], bool]
    )
else:
    FilterCallable = Any

UnknownFields = Literal["ignore", "allow", "deny"]


class SerializeFunc(Generic[T_contra, T_co], Protocol):
    def __call__(self, value: T_contra, **kwargs: Any) -> T_co: ...


class DeserializeFunc(Generic[T, T_contra], Protocol):
    def __call__(self, value: T_contra, cls: type[T], **kwargs: Any) -> T: ...
