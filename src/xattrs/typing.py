# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any, Callable, ClassVar, Protocol, TypeAlias, TypeVar

from dataclasses import Field

from attrs import AttrsInstance


# copy from typeshed/stdlib/dataclasses.pyi
class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


XAttrsInstance = TypeVar("XAttrsInstance", AttrsInstance, DataclassInstance)


A = TypeVar("A")
B = TypeVar("B")


K = TypeVar("K")
V = TypeVar("V")

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
T_pyobj = TypeVar("T_pyobj", Any, None)  # Any Python object
T_proto = TypeVar("T_proto", covariant=True)

# interchange datatype / intermediary / bridge
# Protocol-aware type
# Protocol compatible Python type
T_interm = TypeVar("T_interm")


Predicate: TypeAlias = Callable[[T_pyobj], bool]
T_pred = TypeVar("T_pred", Predicate)

ConstructHook: TypeAlias = Callable[[T_interm, type[T_pyobj]], T_pyobj]
DeconstructHook: TypeAlias = Callable[[T_pyobj], T_interm]

DispatchCallable: TypeAlias = Callable[[type[T_pyobj]], T_pyobj]
T_dpcallable = TypeVar("T_dpcallable", DispatchCallable)

T_hook = TypeVar("T_hook", ConstructHook, DeconstructHook)
HookFactory: TypeAlias = Callable[..., T_hook]
