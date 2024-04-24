# SPDX-FileCopyrightText: 2023-present Lanqing Huang <lqhuang@outlook.com>
#
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from attrs import define as define
from attrs import frozen as frozen

from xattrs.typing import P, R, T_deco, T_fun

__all__ = ["define", "frozen", "derive"]


def derive(*traits: T_deco[P, R]) -> T_deco[P, R]:
    """
    Derive a new class or a new callable with the given traits.

    Simpely compose multiple decorators into one for now.
    """

    def decorator(wrapped: T_fun[P, R]) -> T_fun[P, R]:
        for trait in traits:
            wrapped = trait(wrapped)
        return wrapped

    return decorator
