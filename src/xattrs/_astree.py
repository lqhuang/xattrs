# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations


from copy import copy as shallowcopy
from copy import deepcopy
from functools import partial
from xattrs._compat.typing import Mapping

from xattrs._types import _ATOMIC_TYPES
from xattrs._uni import _is_decorated_instance, _get_fields_func


def astree(inst, *, tuple_factory=tuple, copy=deepcopy):
    """
    Return the fields of a dataclass or attrs instance as a new tuple of field values
    """
    if not _is_decorated_instance(inst):
        raise TypeError("astree() should be called on dataclass or attrs instances")
    return _astree_inner(inst, tuple_factory, copy)


def _astree_inner(inst, tuple_factory, copy):  # noqa: PLR0911, PLR0912
    cls = type(inst)

    if cls in _ATOMIC_TYPES:
        return inst
    elif _is_decorated_instance(inst):
        _fileds = _get_fields_func(inst)

        result = []
        for f in _fileds(inst):
            value = _astree_inner(getattr(inst, f.name), tuple_factory, copy)
            result.append(value)
        return tuple_factory(result)
    elif isinstance(inst, tuple) and hasattr(inst, "_fields"):
        # instance is a namedtuple.
        # keep namedtuple instances as they are, then recurse into their fields.
        return cls(*[_astree_inner(v, tuple_factory, copy) for v in inst])
    elif isinstance(inst, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return cls(_astree_inner(v, tuple_factory, copy) for v in inst)
    elif isinstance(inst, Mapping):
        return tuple(
            (
                _astree_inner(k, tuple_factory, copy),
                _astree_inner(v, tuple_factory, copy),
            )
            for k, v in inst.items()
        )
    else:
        return copy(inst)


_shallow_asdict = partial(astree, copy=shallowcopy)
