# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import TYPE_CHECKING, Callable

from attr import dataclass
from attrs import define, frozen, mutable, field

from xattrs._serde.dict import asdict
from xattrs._serde.tuple import astuple
from xattrs._serde.tree import astree

if TYPE_CHECKING:
    from xattrs.typing import Decorator, P, R_co


__all__ = (
    "derive",
    # from ._serde module
    "asdict",
    "astuple",
    "astree",
    # re-export from attrs
    "dataclass",
    "define",
    "mutable",
    "frozen",
)


def derive(*traits: Decorator[P, R_co]) -> Decorator[P, R_co]:
    """
    Derive a new class or a new `Callable` with the given traits.

    Simpely compose multiple decorators into one for now.
    """

    def decorator(wrapped: Callable[P, R_co]) -> Callable[P, R_co]:
        for trait in traits:
            wrapped = trait(wrapped)
        return wrapped

    return decorator
