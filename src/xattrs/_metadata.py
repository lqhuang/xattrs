# SPDX-License-Identifier: MIT
"""
Read more about Metadata: https://www.attrs.org/en/stable/extending.html#metadata
"""
from __future__ import annotations

from xattrs._compat.typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Mapping,
    TypedDict,
    TypeGuard,
    cast,
    overload,
)
from xattrs._typing import T
from xattrs.typing import CaseConvention, CaseConverter, FilterCallable, StructAs

from dataclasses import Field, asdict, dataclass

from attr._make import _CountingAttr

from xattrs.converters import _CASE_CONVERTER_MAPPING, identity
from xattrs.filters import exclude_if_default as exclude_if_default_filter
from xattrs.filters import exclude_if_false as exclude_if_false_filter
from xattrs.filters import keep_include

if TYPE_CHECKING:
    from attrs import Attribute


@dataclass(slots=True)
class _Metadata(Generic[T]):
    name: str | None = None
    rename: CaseConvention | CaseConverter | None = None
    # rename_ser: str | None = None
    # rename_de: str | None = None

    exclude: bool | None = None
    # exclude_ser: bool = False
    # exclude_de: bool = False
    exclude_if: FilterCallable[T] | None = None
    exclude_if_default: bool | None = None
    exclude_if_false: bool | None = None

    converter_to: Callable[[T], Any] | None = None  # same as converter
    converter_from: Callable[[Any], T] | None = None

    kind: StructAs | None = None
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
    def __ror__(self, value: Field[T]) -> Field[T]: ...
    @overload
    def __ror__(self, value: _CountingAttr) -> _CountingAttr: ...
    def __ror__(self, value: Any) -> Field | _CountingAttr:  # type: ignore[type-arg]
        if isinstance(value, Field):
            metadata = {**value.metadata, **asdict(self)}
            return Field(
                default=cast(T, value.default),
                default_factory=cast(Callable[[], T], value.default_factory),
                init=value.init,
                repr=value.repr,
                hash=value.hash,
                compare=value.compare,
                metadata=metadata,
                kw_only=cast(bool, value.kw_only),
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
    exclude: bool
    exclude_if: FilterCallable | None  # type: ignore[type-arg]
    exclude_if_default: bool | None
    exclude_if_false: bool | None


def _has_filter_params(meta: Mapping) -> TypeGuard[FilterConf]:  # type: ignore[type-arg]
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
    attribute: Field[T] | Attribute[T], scope_filter: FilterCallable[T] | None = None
) -> FilterCallable[T]:
    """Gen a filter function by merging the field and scope filter."""
    _meta = attribute.metadata
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


class RenameConf(TypedDict):
    name: str | None
    rename: CaseConvention | CaseConverter | None


def _has_key_serializer_params(meta: Mapping[str, Any]) -> TypeGuard[RenameConf]:
    return any(
        (
            meta.get("name") is not None,
            meta.get("rename") is not None,
        )
    )


def _gen_field_key_serializer(
    attribute: Field[T] | Attribute[T],
    scope_key_serializer: CaseConverter | None = None,
) -> CaseConverter:
    _meta = attribute.metadata
    if not _has_key_serializer_params(_meta):
        return scope_key_serializer or identity
    if (_name := _meta.get("name")) is not None:
        return lambda x: _name
    elif (_rename := _meta.get("rename")) is not None:
        if isinstance(_rename, str):
            try:
                return _CASE_CONVERTER_MAPPING[_rename]
            except KeyError:
                raise ValueError(
                    f"Invalid case convention value {_rename} for 'rename' in : {attribute!r}."
                ) from None
        else:
            return _rename
    else:
        raise RuntimeError("Unreachable code")
