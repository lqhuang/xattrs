# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import TYPE_CHECKING, Any, ClassVar, Generic

from functools import singledispatch

from xattrs.abc import AbstractDispatcher
from xattrs.base import BaseConstructor
from xattrs.dispatcher import _dispatch_not_found
from xattrs.typing import T, T_interm

if TYPE_CHECKING:
    from xattrs.typing import ConstructHook, Dispatchable

primitive_set: set[Any] = {int, float, str, bool, None, list, tuple}


class Constructor(BaseConstructor[T_interm]):
    """Default concrete constructor"""

    concrete_dispatcher: AbstractDispatcher[T]
    # dict[Dispatchable[T], ConstructHook[T, T_interm]]

    def _dispatched_constructor(self, cls: type[T]) -> ConstructHook[T, T_interm]:
        if cls in primitive_set:
            return self.concrete_dispatcher.dispatch(cls)
        else:
            return self._single_dispatcher.dispatch(cls)

    def construct(self, prim: T_interm, cls: type[Any]) -> Any:
        return self._dispatched_constructor(cls)(prim, cls)

    def _construct_builtin_types(self): ...

    def _construct_generics_types(self): ...
