# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from types import MappingProxyType
from xattrs._compat.typing import Any, Callable, dataclass_transform, overload
from xattrs._typing import AttrsInstance, DataclassInstance, T
from xattrs.typing import (
    CaseConvention,
    CaseConverter,
    FilterBuiltins,
    FilterCallable,
    StructAs,
    UnknownFields,
)

from dataclasses import dataclass

from xattrs._uni import _is_frozen
from xattrs.converters import _CASE_CONVERTER_MAPPING
from xattrs.filters import keep_include

_ATTRS_SERDE = "__attrs_serde__"


@dataclass(slots=True)
class _SerdeParams:
    rename: CaseConvention | CaseConverter | None = None
    # alias: str | None = None
    # alias_converter: str | CaseConvention | None = None
    kind: StructAs | None = None
    filter: FilterBuiltins | FilterCallable | None = None  # type: ignore[type-arg]
    tag: str | Callable | None = None  # type: ignore[type-arg]
    tag_field: str = "type"
    unknown_fields: UnknownFields | None = None
    value_serializer: None = None
    value_deserializer: None = None
    schema: None = None
    metadata: MappingProxyType | None = None  # type: ignore[type-arg]


@overload
def serde(
    cls: type[T],
    /,
    *,
    rename: CaseConvention | None = None,
    kind: StructAs | None = None,
    filter: FilterBuiltins | FilterCallable | None = None,  # type: ignore[type-arg]
    tag: str | Callable | None = None,  # type: ignore[type-arg]
    tag_field: str = "type",
    unknown_fields: UnknownFields | None = None,
    value_serializer: None = None,
    value_deserializer: None = None,
    schema: None = None,
    metadata: MappingProxyType | None = None,  # type: ignore[type-arg]
) -> type[T]: ...


@overload
def serde(
    cls: Any = None,
    /,
    *,
    rename: CaseConvention | CaseConverter | None = None,
    kind: StructAs | None = None,
    filter=None,
    tag: str | Callable | None = None,  # type: ignore[type-arg]
    tag_field: str = "type",
    unknown_fields: UnknownFields | None = None,
    value_serializer: None = None,
    value_deserializer: None = None,
    schema: None = None,
    metadata: MappingProxyType | None = None,  # type: ignore[type-arg]
) -> Callable[[type[T]], type[T]]: ...


@dataclass_transform()
def serde(
    cls: type[T] | None = None,
    /,
    *,
    rename: CaseConvention | CaseConverter | None = None,
    kind: StructAs | None = None,
    filter: FilterBuiltins | FilterCallable | None = None,  # type: ignore[type-arg]
    tag: str | Callable | None = None,  # type: ignore[type-arg]
    tag_field: str = "type",
    unknown_fields: UnknownFields | None = None,
    value_serializer: None = None,
    value_deserializer: None = None,
    schema: None = None,
    metadata: MappingProxyType | None = None,  # type: ignore[type-arg]
):

    def wrapper(cls: type[T]) -> type[T]:
        return _process_serde(  # type: ignore[no-untyped-call,no-any-return]
            cls,
            rename=rename,
            kind=kind,
            filter=filter,
            tag=tag,
            tag_field=tag_field,
            unknown_fields=unknown_fields,
            value_serializer=value_serializer,
            value_deserializer=value_deserializer,
            schema=schema,
            metadata=metadata,
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


def _gen_cls_filter(params: _SerdeParams) -> FilterCallable:  # type: ignore[type-arg]
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
) -> tuple[FilterCallable | None, CaseConvention | None, Callable | None]:  # type: ignore[type-arg]
    """Create per class level filter, key serializer and value serializer from attrs like instance."""
    _serde = _get_serde(obj)
    if _serde is None:
        return None, None, None

    if (filter_ := _serde.filter) is None:
        _filter = None
    else:
        _filter = filter_

    if (rename := _serde.rename) is None:
        _key_serializer = None
    elif isinstance(rename, str):
        try:
            _key_serializer = _CASE_CONVERTER_MAPPING[rename]
        except KeyError:
            raise ValueError(f"unknown alias converter: {rename!r}") from None
    else:
        _key_serializer = rename

    if (val_ser := _serde.value_serializer) is None:
        _value_serializer = None
    else:
        _value_serializer = val_ser

    return _filter, _key_serializer, _value_serializer
