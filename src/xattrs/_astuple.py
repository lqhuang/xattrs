# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations


from copy import copy as shallowcopy
from copy import deepcopy
from functools import partial

from xattrs._types import _ATOMIC_TYPES
from xattrs._uni import _is_decorated_instance, _get_fields_func


def astuple(inst, *, tuple_factory=tuple, copy=deepcopy):
    """
    Return the fields of a dataclass or attrs instance as a new tuple of field values
    """
    if not _is_decorated_instance(inst):
        raise TypeError("astuple() should be called on dataclass or attrs instances")
    return _astuple_inner(inst, tuple_factory, copy)


def _astuple_inner(inst, tuple_factory, copy):  # noqa: PLR0911, PLR0912
    cls = type(inst)

    if cls in _ATOMIC_TYPES:
        return inst
    elif _is_decorated_instance(inst):
        _fileds = _get_fields_func(inst)

        result = []
        for f in _fileds(inst):
            value = _astuple_inner(getattr(inst, f.name), tuple_factory, copy)
            result.append(value)
        return tuple_factory(result)
    elif isinstance(inst, tuple) and hasattr(inst, "_fields"):
        # instance is a namedtuple.
        # keep namedtuple instances as they are, then recurse into their fields.
        return cls(*[_astuple_inner(v, tuple_factory, copy) for v in inst])
    elif isinstance(inst, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return cls(_astuple_inner(v, tuple_factory, copy) for v in inst)
    elif isinstance(inst, dict):
        dict_cls = cls
        if hasattr(dict_cls, "default_factory"):
            # obj is a defaultdict, which has a different constructor from
            # dict as it requires the default_factory as its first arg.
            result = dict_cls.default_factory  # type: ignore
            for k, v in inst.items():
                result[_astuple_inner(k, tuple_factory, copy)] = _astuple_inner(
                    v, tuple_factory, copy
                )
            return result
        return dict_cls(
            (
                _astuple_inner(k, tuple_factory, copy),
                _astuple_inner(v, tuple_factory, copy),
            )
            for k, v in inst.items()
        )
    else:
        return copy(inst)


_shallow_asdict = partial(astuple, copy=shallowcopy)
