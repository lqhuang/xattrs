# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from types import MappingProxyType
from xattrs._compat.typing import Any, Callable, dataclass_transform, overload
from xattrs._typing import AttrsInstance, DataclassInstance, T
from xattrs.typing import (
    CaseConvention,
    FilterType,
    StructAs,
    UnknownFields,
    _ConverterType,
)

from dataclasses import dataclass

from xattrs._uni import _is_frozen
from xattrs.converters import _CASE_CONVERTER_MAPPING
from xattrs.filters import keep_include

_ATTRS_SERDE = "__attrs_serde__"


@dataclass(slots=True)
class _SerdeParams:
    name: str | None = None
    name_converter: _ConverterType | None = None
    alias_converter: str | _ConverterType | None = None
    kind: StructAs | None = "dict"
    filter: FilterType | None = None
    unknown_fields: UnknownFields | None = None
    value_serializer: None = None
    value_deserializer: None = None
    metadata: MappingProxyType | None = None
    schema: None = None

    # alias_map: MappingProxyType | None = field(init=False)


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
    value_serializer=None,
    value_deserializer=None,
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
    value_serializer=None,
    value_deserializer=None,
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
    value_serializer=None,
    value_deserializer=None,
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
            value_serializer=value_serializer,
            value_deserializer=value_deserializer,
            metadata=metadata,
            schema=schema,
        )

    if cls is None:
        return wrapper

    return wrapper(cls)


def _process_serde(cls, **kwargs):
    """Process the `serde` decorator."""
    _serde = _SerdeParams(**kwargs)
    if _is_frozen(cls):
        raise NotImplementedError("Frozen classes are not supported.")
    else:
        setattr(cls, _ATTRS_SERDE, _serde)
    return cls


def _get_serde(obj: Any) -> _SerdeParams | None:
    """Get the `_SerdeParams` object from class or instance."""
    cls = obj if isinstance(obj, type) else type(obj)
    return getattr(cls, _ATTRS_SERDE, None)


def _get_serde_kind(obj: Any) -> StructAs | None:
    _serde = _get_serde(obj)
    return _serde.kind if _serde else None


def _gen_cls_filter(params: _SerdeParams) -> FilterType:
    return keep_include


def _gen_serializer_helpers(
    obj: (
        AttrsInstance
        | DataclassInstance
        | type[AttrsInstance]
        | type[DataclassInstance]
    ),
    /,
    **kwargs,
) -> tuple[FilterType | None, _ConverterType | None, Callable | None]:
    """Create per class level filter, key serializer and value serializer from attrs like instance."""
    _serde = _get_serde(obj)
    if _serde is None:
        return None, None, None

    if (filter_ := _serde.filter) is None:
        _filter = None
    else:
        _filter = filter_

    if (alias_converter := _serde.alias_converter) is None:
        _key_serializer = None
    elif isinstance(alias_converter, str):
        try:
            _key_serializer = _CASE_CONVERTER_MAPPING[alias_converter]  # type: ignore
        except KeyError:
            raise ValueError(f"unknown alias converter: {alias_converter!r}") from None
    else:
        _key_serializer = alias_converter

    if (val_ser := _serde.value_serializer) is None:
        _value_serializer = None
    else:
        _value_serializer = val_ser

    return _filter, _key_serializer, _value_serializer
