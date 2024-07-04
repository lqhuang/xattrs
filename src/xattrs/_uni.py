# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any, Callable

from dataclasses import MISSING, Field
from dataclasses import fields as dataclass_fields

from attr._make import _CountingAttr
from attrs import NOTHING, Attribute
from attrs import fields as attrs_fields

from xattrs._typing import AttrsLike

_ATTRS_ATTRS = "__attrs_attrs__"
_DATACLASS_FIELDS = "__dataclass_fields__"


def _is_attrs_instance(inst: Any) -> bool:
    """Return True if the object is an `attrs` instance."""
    return hasattr(type(inst), _ATTRS_ATTRS)


def _is_dataclass_instance(inst: Any) -> bool:
    """Return True the object is a `dataclass` instance."""
    return hasattr(type(inst), _DATACLASS_FIELDS)


def _is_attrs_like_instance(inst: Any) -> bool:
    """Return True the object is an xattrs instance."""
    return _is_attrs_instance(inst) or _is_dataclass_instance(inst)


def _get_fields_func(inst: Any) -> Callable[[Any], tuple]:
    """Make sure it must a dataclass or attrs instance before calling
    this function"""
    if _is_attrs_instance(inst):
        # `fields` of attrs does not accept an instance, only a class.
        return lambda x: attrs_fields(type(x))
    else:
        return dataclass_fields


def _is_field_like_instance(inst: Any) -> bool:
    if isinstance(inst, (Field, _CountingAttr, Attribute)):
        return True
    else:
        return False


def _should_impl_dataclass(inst: Any) -> bool:
    """Return True if the object should implement the dataclass-like protocol."""
    annotations = getattr(type(inst), "__annotations__", {})
    ...


def _collect_fields(inst: AttrsLike) -> tuple:
    """Collect defined fields if the object has not yet been implemented as
    a dataclass-like class."""
    ...
