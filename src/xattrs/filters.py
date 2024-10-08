# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any, Literal, cast
from xattrs._typing import FieldLike


def keep_include(field: Any, value: Any) -> Literal[True]:
    return True


def exclude_if_default(field: FieldLike[Any], value: Any) -> bool:
    if field.default is not None:
        if not callable(field.default):
            # if not default return True to include
            return cast(bool, value != field.default)
        else:
            raise NotImplementedError("Callable default values are not supported yet.")
    else:
        # no default value
        return True


# TODO: Add test cases
def exclude_if_none(field: FieldLike[Any], value: Any) -> bool:
    return value is not None


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
