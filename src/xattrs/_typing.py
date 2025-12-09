# SPDX-License-Identifier: MIT
from __future__ import annotations

from types import MappingProxyType
from typing import Literal
from xattrs._compat.typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Concatenate,
    Generic,
    LiteralString,
    Mapping,
    ParamSpec,
    Protocol,
    TypeAlias,
    TypeVar,
    TypeVarTuple,
    Union,
)

from dataclasses import Field

from attr._make import _CountingAttr  # noqa: PLC2701
from attrs import Attribute

_T = TypeVar("_T")


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class AttrsInstance(Protocol):
    __attrs_attrs__: ClassVar[tuple[str, Attribute[Any]]]


T_attrs = TypeVar("T_attrs", bound=type[AttrsInstance])
T_dataclass = TypeVar("T_dataclass", bound=type[DataclassInstance])

if TYPE_CHECKING:
    DataclassLike = TypeVar("DataclassLike", DataclassInstance, AttrsInstance)
    FieldLike = Field[_T] | Attribute[_T] | _CountingAttr

    class _DataclassParams:
        init: bool
        repr: bool
        eq: bool
        order: bool
        unsafe_hash: bool
        frozen: bool
        match_args: bool
        kw_only: bool
        slots: bool
        weakref_slot: bool

    class _AttrsParams:
        init: bool
        repr: bool
        eq: bool
        order: bool
        unsafe_hash: bool
        frozen: bool
        match_args: bool
        kw_only: bool
        slots: bool
        weakref_slot: bool

else:
    DataclassLike = Any
    FieldLike = Any

    class _DataclassParams: ...

    class _AttrsParams: ...


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

# T_ls = TypeVar("T_ls", LiteralString)

Decorator: TypeAlias = Callable[[Callable[P, R_co]], Callable[P, R_co]]

if TYPE_CHECKING:
    PredCallable: TypeAlias = Callable[P, bool]
    UnaryCallable: TypeAlias = Callable[Concatenate[T, P], R_co]  # Support at least 1 argument # fmt: skip
    BinaryCallable: TypeAlias = Callable[Concatenate[T1, T2, P], R_co]  # Support at least 2 arguments # fmt: skip
    CallableFacatory: TypeAlias = Callable[P1, Callable[P2, R_co]]

    TreeCallable: TypeAlias = Callable[[tuple[Any]], R_co]
    GenericCallable: TypeAlias = Callable[..., R_co]

else:
    PredCallable = Any
    UnaryCallable = Any
    BinaryCallable = Any
    CallableFacatory = Any

    TreeCallable = Any
    GenericCallable = Any


# ---- Framework specific types ----
# Generic for final protocol type
T_proto = TypeVar("T_proto", covariant=True)
# interchange datatype / intermediary / bridge
# Protocol-aware type
# Protocol compatible Python type
T_interm = TypeVar("T_interm")

if TYPE_CHECKING:
    HookPredicate: TypeAlias = Callable[Concatenate[type[T], P], bool]
    HookFacatory: TypeAlias = Callable[Concatenate[type[T], P], Callable[..., T]]
    ConstructHook: TypeAlias = BinaryCallable[type[T1], T2, ..., T1]
    DeconstructHook: TypeAlias = UnaryCallable[type[T], ..., T]
    Hook = Union[ConstructHook[T, Any], DeconstructHook[T]]
    Dispatchable = Union[type[T], HookPredicate[T, ...]]
else:
    HookPredicate = Any
    HookFacatory = Any
    ConstructHook = Any
    DeconstructHook = Any
    Hook = Any
    Dispatchable = Any


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
