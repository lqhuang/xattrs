# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import dataclass, replace
from functools import partial

__all__ = (
    "dataclass",
    "define",
    "mutable",
    "frozen",
    "evolve",
)

mutable = define = partial(dataclass, slots=True)
frozen = partial(dataclass, frozen=True)
evolve = replace
