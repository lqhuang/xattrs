# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from typing import Mapping
from xattrs._compat.typing import Any

from copy import copy as shallowcopy
from copy import deepcopy
from functools import partial

from xattrs._types import _ATOMIC_TYPES
from xattrs._uni import (
    _get_fields_func,
    _is_attrs_like_instance,
)

__all__ = (
    "asdict",
    "_shallow_asdict",
)


def asdict(
    inst: Any,
    *,
    dict_factory: type[Mapping] = dict,
    key_serializer=None,
    value_serializer=None,
    copy=deepcopy,
) -> Any:
    """
    Return the fields of a dataclass or attrs instance as a new dictionary mapping
    field names to field values.
    """
    return _asdict_inner(inst, dict_factory, key_serializer, value_serializer, copy)


def _asdict_inner(  # noqa: PLR0911, PLR0912
    inst: Any, dict_factory, key_serializer, value_serializer, copy
):
    cls = type(inst)
    args = (key_serializer, value_serializer, copy)

    if cls in _ATOMIC_TYPES:
        return inst
    elif _is_attrs_like_instance(inst):
        # fast path for the common case of a dataclass / attrs instance
        _fileds = _get_fields_func(inst)
        if dict_factory is dict:
            return {
                f.name: _asdict_inner(getattr(inst, f.name), dict, *args)
                for f in _fileds(inst)
            }
        else:
            result = []
            for f in _fileds(inst):
                value = _asdict_inner(getattr(inst, f.name), dict_factory, *args)
                result.append((f.name, value))
            return dict_factory(result)
    elif isinstance(inst, tuple) and hasattr(inst, "_fields"):
        # instance is a namedtuple.
        # keep namedtuple instances as they are, then recurse into their fields.
        return cls(*(_asdict_inner(v, dict_factory, *args) for v in inst))
    elif isinstance(inst, (list, tuple)):
        return cls(_asdict_inner(v, dict_factory, *args) for v in inst)
    elif isinstance(inst, dict):
        if hasattr(cls, "default_factory"):
            # inst is a defaultdict, which has a different constructor from
            # dict as it requires the default_factory as its first arg.
            result = cls.default_factory  # type: ignore
            for k, v in inst.items():
                result[_asdict_inner(k, dict_factory, *args)] = _asdict_inner(
                    v, dict_factory, *args
                )
            return result
        return cls(
            (
                _asdict_inner(k, dict_factory, *args),
                _asdict_inner(v, dict_factory, *args),
            )
            for k, v in inst.items()
        )
    else:
        return copy(inst)


_shallow_asdict = partial(asdict, copy=shallowcopy)
