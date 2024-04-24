# SPDX-FileCopyrightText: 2023-present Lanqing Huang <lqhuang@outlook.com>
#
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Callable

from attrs import define as define
from attrs import frozen as frozen

from xattrs.typing import Decorator, P, R_co

__all__ = ["define", "frozen", "derive"]


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
