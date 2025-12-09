# SPDX-License-Identifier: MIT
from __future__ import annotations

from xattrs._compat.typing import TYPE_CHECKING, Callable

from attr import dataclass
from attrs import define, evolve, field, fields, frozen, mutable

from xattrs._serde import serde
from xattrs._struct_funcs import asdict, astree, astuple

if TYPE_CHECKING:
    from xattrs._typing import Decorator, P, R_co


__all__ = (
    "asdict",
    "astree",
    "astuple",
    "dataclass",
    "define",
    "derive",
    "evolve",
    "field",
    "fields",
    "frozen",
    "mutable",
    "replace",
    "serde",
)

replace = evolve


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
