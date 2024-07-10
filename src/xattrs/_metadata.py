# SPDX-License-Identifier: BSD-3-Clause
"""
Read more about Metadata: https://www.attrs.org/en/stable/extending.html#metadata
"""
from __future__ import annotations

from types import MappingProxyType
from xattrs._compat.typing import (
    Any,
    Callable,
    Generic,
    TypedDict,
    TypeGuard,
    cast,
    overload,
)
from xattrs._typing import Attribute, T, _CountingAttr
from xattrs.typing import CaseConvention, CaseConverter, FilterType, StructAs

from dataclasses import Field, asdict, dataclass

from xattrs.converters import _CASE_CONVERTER_MAPPING, identity
from xattrs.filters import exclude_if_default as exclude_if_default_filter
from xattrs.filters import exclude_if_false as exclude_if_false_filter
from xattrs.filters import keep_include


@dataclass(slots=True)
class _Metadata(Generic[T]):
    alias: str | None = None
    alias_converter: CaseConvention | CaseConverter | None = None
    # alias_ser: str | None = None
    # alias_de: str | None = None

    exclude: bool | None = None
    # exclude_ser: bool = False
    # exclude_de: bool = False
    exclude_if: FilterType[T] | None = None
    exclude_if_default: bool | None = None
    exclude_if_false: bool | None = None

    converter_to: Callable[[T], Any] | None = None  # same as converter
    converter_from: Callable[[Any], T] | None = None

    struct: StructAs | None = None
    flatten: bool = False  # inspired from pyserde

    def __post_init__(self) -> None:
        # check conflicts for exclude params
        num_excludes = sum(
            1 if x is not None else 0
            for x in (
                self.exclude,
                self.exclude_if,
                self.exclude_if_default,
                self.exclude_if_false,
            )
        )
        if num_excludes > 1:
            raise ValueError(
                "Only one of 'exclude', 'exclude_if', 'exclude_if_default', "
                "'exclude_if_false' values can be set."
            )

    @overload
    def __ror__(self, value: Field) -> Field: ...
    @overload
    def __ror__(self, value: _CountingAttr) -> _CountingAttr: ...

    def __ror__(self, value: Any) -> Field | _CountingAttr:
        if isinstance(value, Field):
            metadata = {**value.metadata, **asdict(self)}
            return Field(
                default=value.default,
                default_factory=value.default_factory,  # pyright: ignore[reportArgumentType]
                init=value.init,
                repr=value.repr,
                hash=value.hash,
                compare=value.compare,
                metadata=metadata,
                kw_only=value.kw_only,  # pyright: ignore[reportArgumentType]
            )
        elif isinstance(value, _CountingAttr):
            # avoid to increase cls counter
            value.metadata |= asdict(self)
            return value
        else:
            raise TypeError(
                f"Expected an 'DataclassLike' instance, got {type(value)!r}"
            )


class FilterConf(TypedDict):
    exclude: bool = False
    exclude_if: FilterType[T] | None = None
    exclude_if_default: bool | None = None
    exclude_if_false: bool | None = None


def _has_filter_params(meta: MappingProxyType) -> TypeGuard[FilterConf]:
    return any(
        (
            meta.get("exclude") is not None,
            meta.get("exclude_if") is not None,
            meta.get("exclude_if_default") is not None,
            meta.get("exclude_if_false") is not None,
        )
    )


# FIXME(@lqhuang): update to pipeline scope filter rather than replace scope filter
def _gen_field_filter(
    attribute: Field[T] | Attribute[T], scope_filter: FilterType | None = None
) -> FilterType[T]:
    """Gen a filter function by merging the field and scope filter."""
    _meta = cast(MappingProxyType, attribute.metadata)
    if not _has_filter_params(_meta):
        return scope_filter or keep_include
    elif _meta.get("exclude"):
        return lambda _, __: False  # return False to exclude this field
    elif (exclude_if_filter := _meta.get("exclude_if")) is not None:
        return exclude_if_filter
    elif _meta.get("exclude_if_default"):
        return exclude_if_default_filter
    elif _meta.get("exclude_if_false"):
        return exclude_if_false_filter
    else:
        return keep_include  # only right for replacing scope filter


class AliasConf(TypedDict):
    alias: str | None = None
    alias_converter: CaseConvention | CaseConverter | None = None


def _has_key_serializer_params(meta: MappingProxyType) -> TypeGuard[AliasConf]:
    return any(
        (
            meta.get("alias") is not None,
            meta.get("alias_converter") is not None,
        )
    )


def _gen_field_key_serializer(
    attribute: Field[T] | Attribute[T],
    scope_key_serializer: CaseConverter | None = None,
) -> CaseConverter:
    _meta = cast(MappingProxyType, attribute.metadata)
    if not _has_key_serializer_params(_meta):
        return scope_key_serializer or identity
    if (_alias := _meta.get("alias")) is not None:
        return lambda x: _alias
    elif (_alias_converter := _meta.get("alias_converter")) is not None:
        if isinstance(_alias_converter, str):
            try:
                return _CASE_CONVERTER_MAPPING[_alias_converter]  # type: ignore
            except KeyError:
                raise ValueError(
                    f"Invalid case convention value {_alias_converter} for 'alias_converter' in : {attribute!r}."
                ) from None
        else:
            return _alias_converter
    else:
        raise RuntimeError("Unreachable code")
