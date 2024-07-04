# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any

from enum import Enum

from xattrs._guards import is_enum


def _enum_value(inst: Any, cls: type[Enum]):
    """Return the value from constructed enum instance or itself if it's already enum."""
    if is_enum(inst):
        value = inst.value
        if is_enum(value):
            return _enum_value(value, type(value))
        else:
            return value
    else:
        return cls(inst).value
