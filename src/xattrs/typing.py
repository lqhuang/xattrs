# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import (
    Any,
    Callable,
    Generic,
    Literal,
    Protocol,
    TYPE_CHECKING,
)

from attrs import Attribute

from xattrs._typing import T, T_co, T_contra

StructAs = Literal["dict", "tuple", "tree"] | None

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
UnknownFields = Literal["ignore", "allow", "deny"]


class SerializeFunc(Generic[T_contra, T_co], Protocol):
    def __call__(self, value: T_contra, **kwargs: Any) -> T_co: ...


class DeserializeFunc(Generic[T, T_contra], Protocol):
    def __call__(self, value: T_contra, cls: type[T], **kwargs: Any) -> T: ...


_ConverterType = Callable[[Any], Any]
if TYPE_CHECKING:
    _FilterType = Callable[[Attribute[T], T], bool]
else:
    _FilterType = Any
