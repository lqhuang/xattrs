# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from typing import Callable, Mapping
from xattrs._compat.typing import Any

from copy import copy as shallowcopy
from copy import deepcopy
from dataclasses import fields as dataclass_fields
from functools import partial

from attrs import fields as attrs_fields

from xattrs._types import _ATOMIC_TYPES
from xattrs._uni import (
    _is_attrs_instance,
    _is_dataclass_instance,
    _is_decorated_instance,
    _get_fields_func,
)

__all__ = (
    "asdict",
    "_shallow_asdict",
)


def asdict(inst: Any, *, dict_factory=dict, deconstructor=None, copy=deepcopy) -> Any:
    """
    Return the fields of a dataclass or attrs instance as a new dictionary mapping
    field names to field values.
    """
    if not _is_decorated_instance(inst):
        raise TypeError("asdict() should be called on dataclass or attrs instances")
    return _asdict_inner(inst, dict_factory, copy)


def _asdict_inner(inst: Any, dict_factory, copy):  # noqa: PLR0911, PLR0912
    if type(inst) in _ATOMIC_TYPES:
        return inst
    elif _is_decorated_instance(inst):
        # fast path for the common case of a dataclass / attrs instance
        _fileds = _get_fields_func(inst)
        if dict_factory is dict:
            return {
                f.name: _asdict_inner(getattr(inst, f.name), dict, copy)
                for f in _fileds(inst)
            }
        else:
            result = []
            for f in _fileds(inst):
                value = _asdict_inner(getattr(inst, f.name), dict_factory, copy)
                result.append((f.name, value))
            return dict_factory(result)
    elif isinstance(inst, tuple) and hasattr(inst, "_fields"):
        # instance is a namedtuple.
        # keep namedtuple instances as they are, then recurse into their fields.
        return type(inst)(*(_asdict_inner(v, dict_factory, copy) for v in inst))
    elif isinstance(inst, (list, tuple)):
        return type(inst)(_asdict_inner(v, dict_factory, copy) for v in inst)
    elif isinstance(inst, dict):
        if hasattr(type(inst), "default_factory"):
            # inst is a defaultdict, which has a different constructor from
            # dict as it requires the default_factory as its first arg.
            result = type(inst).default_factory  # type: ignore
            for k, v in inst.items():
                result[_asdict_inner(k, dict_factory, copy)] = _asdict_inner(
                    v, dict_factory, copy
                )
            return result
        return type(inst)(
            (_asdict_inner(k, dict_factory, copy), _asdict_inner(v, dict_factory, copy))
            for k, v in inst.items()
        )
    else:
        return copy(inst)


_shallow_asdict = partial(asdict, copy=shallowcopy)
