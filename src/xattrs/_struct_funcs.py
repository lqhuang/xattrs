# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from typing import Mapping
from xattrs._compat.typing import Any, Callable

from copy import copy as shallowcopy
from copy import deepcopy
from functools import partial

from xattrs._helpers import _identity
from xattrs._serde import _get_serde
from xattrs._types import _ATOMIC_TYPES
from xattrs._uni import _get_fields_func, _is_dataclass_like_instance
from xattrs.serializer import _make_serializer
from xattrs.typing import StructAs

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
    elif _is_dataclass_like_instance(inst):
        # fast path for the common case of a dataclass / attrs instance
        _fileds = _get_fields_func(inst)

        _serde = _get_serde(inst)
        if _serde is None:
            as_func = _asdict_inner
            _key_serializer = key_serializer or _identity
        else:
            as_func = (
                _asdict_inner if _serde.kind is None else _AS_FUNCS_MAPPING[_serde.kind]
            )
            inst_key_serializer, _inst_val_serializer = _make_serializer(inst)
            _key_serializer = inst_key_serializer or key_serializer or _identity

        if dict_factory is dict:
            return {
                _key_serializer(f.name): as_func(getattr(inst, f.name), dict, *args)
                for f in _fileds(inst)
            }
        else:
            result = []
            for f in _fileds(inst):
                value = as_func(getattr(inst, f.name), dict_factory, *args)
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


def astuple(
    inst,
    *,
    tuple_factory=tuple,
    key_serializer=None,
    value_serializer=None,
    copy=deepcopy,
):
    """
    Return the fields of a dataclass or attrs instance as a new tuple of field values
    """
    return _astuple_inner(inst, tuple_factory, key_serializer, value_serializer, copy)


def _astuple_inner(  # noqa: PLR0911, PLR0912
    inst, tuple_factory, key_serializer, value_serializer, copy
):
    args = (key_serializer, value_serializer, copy)
    cls = type(inst)

    if cls in _ATOMIC_TYPES:
        return inst
    elif _is_dataclass_like_instance(inst):
        _fileds = _get_fields_func(inst)

        result = []
        for f in _fileds(inst):
            value = _astuple_inner(getattr(inst, f.name), tuple_factory, *args)
            result.append(value)
        return tuple_factory(result)
    elif isinstance(inst, tuple) and hasattr(inst, "_fields"):
        # instance is a namedtuple.
        # keep namedtuple instances as they are, then recurse into their fields.
        return cls(*[_astuple_inner(v, tuple_factory, *args) for v in inst])
    elif isinstance(inst, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return cls(_astuple_inner(v, tuple_factory, *args) for v in inst)
    elif isinstance(inst, dict):
        dict_cls = cls
        if hasattr(dict_cls, "default_factory"):
            # obj is a defaultdict, which has a different constructor from
            # dict as it requires the default_factory as its first arg.
            result = dict_cls.default_factory  # type: ignore
            for k, v in inst.items():
                result[_astuple_inner(k, tuple_factory, *args)] = _astuple_inner(
                    v, tuple_factory, *args
                )
            return result
        return dict_cls(
            (
                _astuple_inner(k, tuple_factory, *args),
                _astuple_inner(v, tuple_factory, *args),
            )
            for k, v in inst.items()
        )
    else:
        return copy(inst)


def astree(
    inst,
    *,
    tuple_factory=tuple,
    key_serializer=None,
    value_serializer=None,
    copy=deepcopy,
):
    """
    Return the fields of a dataclass or attrs instance as a new tuple of field values
    """
    return _astree_inner(inst, tuple_factory, key_serializer, value_serializer, copy)


def _astree_inner(  # noqa: PLR0911, PLR0912
    inst, tuple_factory, key_serializer, value_serializer, copy
):
    args = (key_serializer, value_serializer, copy)
    cls = type(inst)

    if cls in _ATOMIC_TYPES:
        return inst
    elif _is_dataclass_like_instance(inst):
        _fileds = _get_fields_func(inst)

        result = []
        for f in _fileds(inst):
            value = _astree_inner(getattr(inst, f.name), tuple_factory, *args)
            result.append(value)
        return tuple_factory(result)
    elif isinstance(inst, tuple) and hasattr(inst, "_fields"):
        # instance is a namedtuple.
        # keep namedtuple instances as they are, then recurse into their fields.
        return cls(*[_astree_inner(v, tuple_factory, *args) for v in inst])
    elif isinstance(inst, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return cls(_astree_inner(v, tuple_factory, *args) for v in inst)
    elif isinstance(inst, Mapping):
        return tuple(
            (
                _astree_inner(k, tuple_factory, *args),
                _astree_inner(v, tuple_factory, *args),
            )
            for k, v in inst.items()
        )
    else:
        return copy(inst)


_shallow_asdict = partial(asdict, copy=shallowcopy)
_shallow_astuple = partial(astuple, copy=shallowcopy)
_shallow_astree = partial(astree, copy=shallowcopy)

_AS_FUNCS_MAPPING: dict[StructAs, Callable] = {
    "dict": _asdict_inner,
    "tuple": _astuple_inner,
    "tree": _astree_inner,
}
