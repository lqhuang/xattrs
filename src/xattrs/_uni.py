# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any, Callable

from dataclasses import MISSING
from dataclasses import fields as dataclass_fields
from dataclasses import is_dataclass

from attrs import NOTHING, AttrsInstance
from attrs import fields as attrs_fields

_ATTRS_ATTRS = "__attrs_attrs__"
_DATACLASS_FIELDS = "__dataclass_fields__"


def _is_attrs_instance(inst: Any) -> bool:
    """Return True if the object is an `attrs` instance."""
    return hasattr(type(inst), _ATTRS_ATTRS)


def _is_dataclass_instance(inst: Any) -> bool:
    """Return True the object is a `dataclass` instance."""
    return hasattr(type(inst), _DATACLASS_FIELDS)


def _is_decorated_instance(inst: Any) -> bool:
    """Return True the object is an xattrs instance."""
    return _is_attrs_instance(inst) or _is_dataclass_instance(inst)


def _get_fields_func(inst: Any) -> Callable[[Any], tuple]:
    """Make sure it must a dataclass or attrs instance before calling this function"""
    if _is_attrs_instance(inst):
        # `fields` of attrs does not accept an instance, only a class.
        return lambda x: attrs_fields(type(x))
    else:
        return dataclass_fields


def has(cls: type) -> bool:
    """Check whether **cls** is a class with `attrs` attributes or `dataclass` fields."""
    return hasattr(cls, _ATTRS_ATTRS) or hasattr(cls, _DATACLASS_FIELDS)
