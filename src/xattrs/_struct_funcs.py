# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from typing import Mapping
from xattrs._compat.typing import Any, Callable, Hashable

from copy import copy as shallowcopy
from copy import deepcopy
from functools import partial

from xattrs._helpers import _identity
from xattrs._serde import _get_serde, _gen_serializer_helpers
from xattrs._types import _ATOMIC_TYPES
from xattrs._uni import _fields, _is_data_class_like_instance

from xattrs.typing import StructAs
from xattrs._typing import T
from xattrs._metadata import _gen_field_filter, _gen_field_key_serializer
from xattrs.filters import keep_include

__all__ = (
    "asdict",
    "asdict_shallow",
    "astuple",
    "astuple_shallow",
    "astree",
    "astree_shallow",
)


def _as_primitive(
    inst: Any,
    *,
    factory: Callable[[], T],
    filter=None,
    key_serializer=None,
    value_serializer=None,
    copy=deepcopy,
) -> T:
    if isinstance(inst, type):
        raise ValueError("Must be an instance")

    cls = type(inst)

    if cls in _ATOMIC_TYPES:
        return inst
    elif _is_data_class_like_instance(inst):
        inst_fields = _fields(inst)
        inst_serde_params = _get_serde(inst) or {}

        cls_key_serializer = key_serializer or _identity
        cls_value_serializer = value_serializer or _identity

    raise NotImplementedError


def asdict(
    inst: Any,
    *,
    dict_factory: type[Mapping] = dict,
    filter=None,
    key_serializer=None,
    value_serializer=None,
    copy=deepcopy,
) -> Mapping[Hashable, Any]:
    """
    Return the fields of a dataclass or attrs instance as a new dictionary mapping
    field names to field values.
    """
    if isinstance(inst, type):
        raise TypeError("Must be an instance")
    return _asdict_inner(
        inst, dict_factory, filter, key_serializer, value_serializer, copy
    )


def _asdict_inner(  # noqa: PLR0911, PLR0912
    inst: Any, dict_factory, filter_, key_serializer, value_serializer, copy
):
    cls = type(inst)
    args = (filter_, key_serializer, value_serializer, copy)

    if cls in _ATOMIC_TYPES:
        return inst
    elif _is_data_class_like_instance(inst):
        # fast path for the common case of a dataclass / attrs instance
        _serde = _get_serde(inst)

        inst_filter, inst_key_ser, inst_val_ser = _gen_serializer_helpers(inst)
        _filter = inst_filter or filter_ or keep_include
        _key_ser = inst_key_ser or key_serializer or _identity
        _val_ser = inst_val_ser or value_serializer or _identity

        pairs = (
            (
                _gen_field_key_serializer(f, _key_ser)(f.name),
                _asdict_inner(getattr(inst, f.name), dict_factory, *args),
            )
            for f in _fields(inst)
            if _gen_field_filter(f, _filter)(f, getattr(inst, f.name))
        )
        return dict_factory(pairs)
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
    elif _is_data_class_like_instance(inst):
        result = []
        for f in _fields(inst):
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
    elif _is_data_class_like_instance(inst):
        result = []
        for f in _fields(inst):
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


asdict_shallow = partial(asdict, copy=shallowcopy)
astuple_shallow = partial(astuple, copy=shallowcopy)
astree_shallow = partial(astree, copy=shallowcopy)

_AS_FUNCS_MAPPING: dict[StructAs, Callable] = {
    "dict": _asdict_inner,
    "tuple": _astuple_inner,
    "tree": _astree_inner,
}
