# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations


from dataclasses import Field, asdict, dataclass

from attr._make import _CountingAttr

from xattrs._types import CaseConvention
from xattrs.typing import AttributeLike


@dataclass(frozen=True, slots=True)
class _Metadata:
    case_convention: CaseConvention | None = None

    alias: str | None = None
    alias_ser: str | None = None
    alias_de: str | None = None

    skip: bool = False
    skip_ser: bool = False
    skip_de: bool = False

    skip_if: bool = False
    skip_unless: bool = False
    skip_if_none: bool = False

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
