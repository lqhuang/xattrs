# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._uni import _ATTRS_ATTRS, _DATACLASS_FIELDS


def has(cls: type) -> bool:
    """Check whether **cls** is a class with `attrs` attributes or `dataclass` fields."""
    return hasattr(cls, _ATTRS_ATTRS) or hasattr(cls, _DATACLASS_FIELDS)
