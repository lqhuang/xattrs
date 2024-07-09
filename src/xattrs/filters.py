# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any
from xattrs._typing import FieldLike


def keep_include(field: Any, value: Any) -> True:
    return True


def exclude_if_default(field: FieldLike, value: Any) -> bool:
    if field.default is not None:
        return value != field.default  # if not default return True to include
    else:
        # no default value
        return True


def exclude_if_false(field: Any, value: Any) -> bool:
    """
    >>> True if 0 else False
    >>> False
    >>> True if [] else False
    >>> False

    >>> bool(0)
    >>> False
    >>> bool([])
    >>> False
    """
    return bool(value)
