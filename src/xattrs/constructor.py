# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any, ClassVar

from functools import _SingleDispatchCallable, singledispatch

from xattrs.base import BaseConstructor
from xattrs.helpers import single_dispatch_not_found
from xattrs.typing import ConstructHook, T_interm

primitive_set: set[Any] = {int, float, str, bool, None, list, tuple}


class Constructor(BaseConstructor[T_interm]):
    """Default concrete constructor"""

    _exacth_dispatcher: ClassVar[dict[type[Any], ConstructHook[T_interm]]] = {}
    _single_dispatcher: ClassVar[_SingleDispatchCallable] = singledispatch(
        single_dispatch_not_found
    )
    _union_dispatcher: ClassVar[_SingleDispatchCallable] = singledispatch()
    _hook_dispatcher: ClassVar[_SingleDispatchCallable] = singledispatch()

    def _dispatched_constructor(self, cls: type[Any]) -> ConstructHook[T_interm]:
        if cls in primitive_set:
            return self._exacth_dispatcher[cls]
        else:
            return self._single_dispatcher.dispatch(cls)

    def construct(self, prim: T_interm, cls: type[Any]) -> Any:
        return self._dispatched_constructor(cls)(prim, cls)

    def _construct_builtin_types(self): ...

    def _construct_generics_types(self): ...
