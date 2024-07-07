# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from types import MappingProxyType
from xattrs._compat.typing import (
    Any,
    Callable,
    ClassVar,
    Concatenate,
    Generic,
    ParamSpec,
    Protocol,
    TypeAlias,
    TypeVar,
    TypeVarTuple,
    Union,
    TYPE_CHECKING,
)

from dataclasses import Field

from attrs import Attribute
from attr._make import _CountingAttr


if TYPE_CHECKING:

    class DataclassInstance(Protocol):
        __dataclass_fields__: ClassVar[dict[str, Field[Any]]]

    class AttrsInstance(Protocol):
        __attrs_attrs__: ClassVar[tuple[str, Attribute[Any]]]

    AttrsLike = TypeVar("AttrsLike", DataclassInstance, AttrsInstance)
    AttributeLike = TypeVar("AttributeLike", Field[Any], Attribute[Any], _CountingAttr)

else:

    class DataclassInstance(Protocol): ...

    class AttrsInstance(Protocol): ...

    AttrsLike = Any
    AttributeLike = Any


S = TypeVar("S", bound=str)
A = TypeVar("A")
B = TypeVar("B")

K = TypeVar("K")
V = TypeVar("V")

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)

P = ParamSpec("P")
P1 = ParamSpec("P1")
P2 = ParamSpec("P2")
R_co = TypeVar("R_co", covariant=True)
Ts = TypeVarTuple("Ts")

Decorator: TypeAlias = Callable[[Callable[P, R_co]], Callable[P, R_co]]

PredCallable: TypeAlias = Callable[P, bool]
UnaryCallable: TypeAlias = Callable[Concatenate[T, P], R_co]  # Support at least 1 argument # fmt: skip
BinaryCallable: TypeAlias = Callable[Concatenate[T1, T2, P], R_co]  # Support at least 2 arguments # fmt: skip
CallableFacatory: TypeAlias = Callable[P1, Callable[P2, R_co]]

TreeCallable: TypeAlias = Callable[[tuple[Any]], R_co]
GenericCallable: TypeAlias = Callable[..., R_co]


######## Framework specific types ########
# Generic for final protocol type
T_proto = TypeVar("T_proto", covariant=True)  # noqa: PLC0105
# interchange datatype / intermediary / bridge
# Protocol-aware type
# Protocol compatible Python type
T_interm = TypeVar("T_interm")

HookPredicate: TypeAlias = Callable[Concatenate[type[T], P], bool]
HookFacatory: TypeAlias = Callable[Concatenate[type[T], P], Callable[..., T]]
ConstructHook: TypeAlias = BinaryCallable[type[T1], T2, ..., T1]
DeconstructHook: TypeAlias = UnaryCallable[type[T], ..., T]
Hook = Union[ConstructHook[T, Any], DeconstructHook[T]]
Dispatchable = Union[type[T], HookPredicate[T, ...]]


class SingleDispatchCallable(Generic[T]):
    """polymorphism on single parameter"""

    registry: MappingProxyType[Any, GenericCallable[T]]

    def register(
        self, cls: type[T], func: GenericCallable[T]
    ) -> GenericCallable[T]: ...
    def dispatch(self, cls: type[T]) -> GenericCallable[T]: ...
    def _clear_cache(self) -> None: ...
    def __call__(self, /, *args: Any, **kwargs: Any) -> T: ...


class UnarySingleDispatchCallable(SingleDispatchCallable[T]):
    # fmt: off
    def register(self, cls: type[T], func: UnaryCallable[T, ..., T]) -> UnaryCallable[T, ..., T]: ...
    def dispatch(self, cls: type[T]) -> UnaryCallable[T, ..., T]: ...
    # fmt: on


class TreeSingleDispatchCallable(SingleDispatchCallable[T]):
    def register(self, cls: type[T], func: TreeCallable[T]) -> TreeCallable[T]: ...
    def dispatch(self, cls: type[T]) -> TreeCallable[T]: ...


class PredicateSingleDispatchCallable:
    # fmt: off
    def register(self, pred: PredCallable[P], func: GenericCallable[T]) -> GenericCallable[T]: ...
    def dispatch(self, pred: PredCallable[P]) -> GenericCallable[T]: ...
    # fmt: on
