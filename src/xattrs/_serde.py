# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from types import MappingProxyType
from xattrs._compat.typing import Any, Callable, dataclass_transform, overload

from dataclasses import dataclass

from xattrs._typing import T
from xattrs.typing import (
    CaseConvention,
    StructAs,
    UnknownFields,
    _ConverterType,
    _FilterType,
)

_XATTRS_SERDE = "__xattrs_serde__"


@dataclass(frozen=True, slots=True)
class _XattrsSerde:
    name: str | None = None
    name_converter: _ConverterType | None = None
    alias_converter: str | _ConverterType | None = None
    kind: StructAs | None = "dict"
    filter: _FilterType | None = None
    unknown_fields: UnknownFields | None = None
    serializer: None = None
    deserializer: None = None
    metadata: MappingProxyType | None = None
    schema: None = None


@overload
def serde(
    cls: type[T],
    /,
    *,
    name: str | None = None,
    name_converter: _ConverterType | None = None,
    alias_converter: CaseConvention | None = None,
    filter=None,
    unknown_fields: UnknownFields | None = None,
    serializer=None,
    deserializer=None,
    metadata=None,
    schema=None,
) -> type[T]: ...


@overload
def serde(
    cls: Any = None,
    /,
    *,
    name: str | None = None,
    name_converter: _ConverterType | None = None,
    alias_converter: CaseConvention | None = None,
    filter=None,
    unknown_fields: UnknownFields | None = None,
    serializer=None,
    deserializer=None,
    metadata=None,
    schema=None,
) -> Callable[[type[T]], type[T]]: ...


@dataclass_transform()
def serde(
    cls=None,
    /,
    *,
    name=None,
    name_converter=None,
    alias_converter=None,
    filter=None,
    unknown_fields=None,
    serializer=None,
    deserializer=None,
    metadata=None,
    schema=None,
):

    def wrapper(cls):
        return _process_serde(
            cls,
            name=name,
            name_converter=name_converter,
            alias_converter=alias_converter,
            filter=filter,
            unknown_fields=unknown_fields,
            serializer=serializer,
            deserializer=deserializer,
            metadata=metadata,
            schema=schema,
        )

    if cls is None:
        return wrapper

    return wrapper(cls)


def _process_serde(cls, **kwargs):
    """Process the `serde` decorator."""
    setattr(cls, _XATTRS_SERDE, _XattrsSerde(**kwargs))
    return cls


def _get_xattrs_serde(cls: Any) -> _XattrsSerde | None:
    """Get the `_XattrsSerde` object."""
    return getattr(cls, _XATTRS_SERDE, None)


def _make_key_deconstructor(cls: Any) -> Callable[[str], str]:
    """Make a key deconstructor."""

    _serde = _get_xattrs_serde(cls)

    key_transformer = _serde.name_converter

    return key_deconstructor(key_transformer)
