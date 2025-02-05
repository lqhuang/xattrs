# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import dataclass, replace
from functools import partial

__all__ = (
    "dataclass",
    "define",
    "evolve",
    "frozen",
    "mutable",
)

mutable = define = partial(dataclass, slots=True)
frozen = partial(dataclass, frozen=True)
evolve = replace
