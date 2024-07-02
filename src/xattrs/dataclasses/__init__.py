# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from dataclasses import dataclass
from functools import partial

__all__ = (
    "dataclass",
    "define",
    "mutable",
    "frozen",
)

mutable = define = partial(dataclass, slots=True)
frozen = partial(dataclass, frozen=True)
