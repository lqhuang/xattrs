# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import TYPE_CHECKING, Callable

from attr import dataclass
from attr._funcs import evolve
from attr._make import fields
from attrs import define, field, frozen, mutable

from xattrs._serde import serde
from xattrs._struct_funcs import asdict, astree, astuple

if TYPE_CHECKING:
    from xattrs._typing import Decorator, P, R_co


__all__ = (
    "derive",
    # from ._struct_funcs module
    "asdict",
    "astuple",
    "astree",
    # re-export from attrs
    "dataclass",
    "define",
    "mutable",
    "frozen",
    "field",
    # re-export funcs from attrs
    "fields",
    "evolve",
    "replace",
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
