# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Callable

from dataclasses import Field, asdict, dataclass

from attr._make import _CountingAttr

from xattrs._typing import AttributeLike
from xattrs.typing import CaseConvention

# @dataclass(frozen=True, slots=True)
# class AliasOverride:
#     ser
CaseConverter = Callable[[str], str]


@dataclass(frozen=True, slots=True)
class _Metadata:

    alias_converter: CaseConvention | CaseConverter | None = None
    alias_ser: str | None = None
    alias_de: str | None = None

    exclude: bool = False
    exclude_ser: bool = False
    exclude_de: bool = False

    exclude_if: Callable | None = None
    exclude_unless: bool | None = None
    exclude_if_default: bool | None = None

    def __ror__(self, value: AttributeLike) -> AttributeLike:
        if isinstance(value, Field):
            metadata = value.metadata | asdict(self)
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
                f"Expected an 'AttributeLike' instance, got {type(value)!r}"
            )
