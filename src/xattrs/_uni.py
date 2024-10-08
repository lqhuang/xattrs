# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any, TypeGuard, cast, overload
from xattrs._typing import (
    AttrsInstance,
    DataclassInstance,
    DataclassLike,
    _AttrsParams,
    _DataclassParams,
)

from dataclasses import MISSING, Field
from dataclasses import fields as dataclass_fields
from dataclasses import is_dataclass

from attr._make import _CountingAttr
from attrs import NOTHING, Attribute
from attrs import fields as attrs_fields

_ATTRS_ATTRS = "__attrs_attrs__"
_DATACLASS_FIELDS = "__dataclass_fields__"
_DATACLASS_PARAMS = "_dataclass_params__"


def _is_attrs_instance(inst: Any) -> TypeGuard[AttrsInstance]:
    """Return True if the object is an instance of a attrs."""
    return hasattr(type(inst), _ATTRS_ATTRS)


def _is_attrs_class(cls: type) -> TypeGuard[type[AttrsInstance]]:
    """Returns True if object is an attrs class"""
    return hasattr(cls, _ATTRS_ATTRS)


def _is_attrs(obj: Any | type) -> TypeGuard[AttrsInstance | type[AttrsInstance]]:
    """Returns True if object is an attrs or an instance of an attrs."""
    cls = obj if isinstance(obj, type) else type(obj)
    return _is_attrs_class(cls)


def _is_dataclass_instance(inst: Any) -> TypeGuard[DataclassInstance]:
    """Return True if the object is an instance of a dataclass."""
    return hasattr(type(inst), _DATACLASS_FIELDS)


def _is_dataclass_class(cls: type) -> TypeGuard[type[DataclassInstance]]:
    """Returns True if object is a dataclass class"""
    return hasattr(cls, _DATACLASS_FIELDS)


def _is_dataclass(
    obj: Any | type,
) -> TypeGuard[DataclassInstance | type[DataclassInstance]]:
    """Returns True if object is a dataclass or an instance of a dataclass."""
    return is_dataclass(obj)


def _is_data_class_like(obj: Any | type) -> bool:
    """Return True if the object is a dataclass like class or
    a instance of a dataclass like class."""
    return _is_dataclass(obj) or _is_attrs(obj)


def _is_data_class_like_instance(obj: Any) -> bool:
    """Return True if the object is an instance of a dataclass like class."""
    return _is_dataclass_instance(obj) or _is_attrs_instance(obj)


@overload
def _get_params(
    obj: DataclassInstance | type[DataclassInstance],
) -> _DataclassParams: ...


@overload
def _get_params(
    obj: AttrsInstance | type[AttrsInstance],
) -> _AttrsParams: ...


def _get_params(obj: Any) -> _DataclassParams | _AttrsParams:
    """Return the parameters of the dataclass-like instance."""
    cls = obj if isinstance(obj, type) else type(obj)
    if _is_attrs_class(cls):
        raise NotImplementedError("attrs instance is not supported yet.")
    elif is_dataclass(cls):
        return getattr(cls, _DATACLASS_PARAMS)
    else:
        raise TypeError("The object is not a dataclass-like type.")


@overload
def _fields(obj: DataclassInstance | type[DataclassInstance]) -> tuple[Field]: ...


@overload
def _fields(obj: AttrsInstance | type[AttrsInstance]) -> tuple[Attribute]: ...


def _fields(obj: Any) -> tuple[Attribute[Any]] | tuple[Field[Any]]:
    """Return a tuple describing the fields of this dataclass or attrs.

    Accepts a dataclass (attrs) or an instance of one. Tuple elements are of
    type Field (Attribute if attrs).
    """
    if not _is_data_class_like(obj):
        raise TypeError(
            "must be called with a data class like (attrs/dataclass) type or instance"
        )

    cls = obj if isinstance(obj, type) else type(obj)
    if _is_attrs_class(cls):
        # `fields` of attrs does not accept an instance, only a class.
        return attrs_fields(cls)
    else:
        return dataclass_fields(cls)  # pyright: ignore[reportReturnType]


def _is_field_like_instance(inst: Any) -> bool:
    if isinstance(inst, (Field, _CountingAttr, Attribute)):
        return True
    else:
        return False


def _should_impl_dataclass(cls: type) -> bool:
    """Return True if the object should implement the dataclass-like protocol."""
    return not _is_data_class_like(cls)


def _collect_fields(inst: DataclassLike) -> tuple:
    """Collect defined fields if the object has not yet been implemented as
    a dataclass-like class."""
    ...


def _is_frozen(cls: Any) -> bool:
    """Return True if the object is frozen."""
    if _is_attrs_class(cls):
        return not hasattr(cls, "__attrs_own_setattr__")
    elif _is_dataclass_class(cls):
        return cast(_DataclassParams, getattr(cls, _DATACLASS_PARAMS)).frozen
    else:
        raise TypeError("The object is not a dataclass-like instance or class.")
