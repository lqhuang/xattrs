# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any

from xattrs._helpers import _identity
from xattrs._serde import _get_serde
from xattrs._typing import AttrsInstance, DataclassInstance, T_interm, T_proto
from xattrs.base import BaseSerializer
from xattrs.converters import _CASE_CONVERTER_MAPPING


class Serializer(BaseSerializer[T_interm, T_proto]): ...


_KeySerializer = Any
_ValueSerializer = Any


def _make_serializer(
    obj: (
        AttrsInstance
        | DataclassInstance
        | type[AttrsInstance]
        | type[DataclassInstance]
    ),
    /,
    **kwargs,
) -> tuple[_KeySerializer, _ValueSerializer]:
    """Create key serializer and value serializer from the given attrs-like
    class or instance."""

    _serde = _get_serde(obj)
    if _serde is None:
        raise TypeError(f"unsupported object: {obj!r}")

    if (alias_converter := _serde.alias_converter) is None:
        _key_serializer = _identity
    elif isinstance(alias_converter, str):
        try:
            _key_serializer = _CASE_CONVERTER_MAPPING[alias_converter]  # type: ignore
        except KeyError:
            raise ValueError(f"unknown alias converter: {alias_converter!r}") from None
    else:
        _key_serializer = alias_converter

    if (serializer := _serde.serializer) is None:
        _value_serializer = _identity
    else:
        _value_serializer = serializer

    return _key_serializer, _value_serializer
