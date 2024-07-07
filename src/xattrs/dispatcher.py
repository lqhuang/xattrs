# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from typing import NoReturn
from xattrs._compat.typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Final,
    Mapping,
    cast,
)

from functools import singledispatch

from xattrs.abc import AbstractDispatcher
from xattrs.exceptions import HookNotFoundError
from xattrs.typing import SingleDispatchCallable, T, UnarySingleDispatchCallable

if TYPE_CHECKING:
    from xattrs.typing import Dispatchable, Hook


def _dispatch_not_found(_, **kwargs) -> NoReturn:
    raise HookNotFoundError("Hook not found. This raised by not found fallback hook.")


_unary_hook_registry: dict[type[T], Callable[[Any], T]] = {
    # builtin types
    # error/exception types
    # warning types
}

# slice: lambda x: slice(x),
_error_hook = {}
_warning_hook = {}

# generic types:
# tuple: lambda x: tuple(x),
# list: lambda x: list(x),
# set: lambda x: set(x),
# dict: lambda x: dict(x),
# frozenset: lambda x: frozenset(x)


class ConcreteDispatch(AbstractDispatcher[T]):
    """Dispatch for concrete types."""

    _registry: dict[type[T], Hook[T]] = _unary_hook_registry  # pyright: ignore[reportAssignmentType] # fmt: skip

    # def register(self, cls: Dispatchable[T], func: Hook[T]) -> Hook[T]:
    #     self._registry[cls] = func
    #     return func

    def dispatch(self, cls: type[T]) -> Hook[T]:
        hook = self._registry.get(cls)
        if hook is None:
            raise HookNotFoundError(f"Hook for {cls} not found.")
        return hook


class SingleDispatcher(AbstractDispatcher[T]):
    """Single dispatch dispatcher

    This is a dispatcher that uses the ``singledispatch`` function for ``covariant`` types.
    """

    _registry: ClassVar[...]

    def __init__(self) -> None:
        self._singledispatch = singledispatch(_dispatch_not_found)

    def register(self, cls: type[T], func: Hook[T]) -> Hook[T]:
        return self._singledispatch.register(cls, func)

    def dispatch(self, cls: type[T]) -> Hook[T]:
        return self._singledispatch.dispatch(cls)


class GenericDispatcher:
    """Generic dispatcher

    This is a dispatcher that uses the ``singledispatch`` function for ``contravariant`` types.
    """

    _registry: ClassVar
