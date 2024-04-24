# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Any, ClassVar, TypeVar, Union

from enum import Enum

from xattrs.base import BaseDeconstructor
from xattrs.typing import T_interm


class DeconstructStrategy(Enum):
    """``attrs``/``dataclass`` classes deconstructing strategies."""

    AS_DICT = "as_dict"
    AS_TUPLE = "as_tuple"
    AS_LIST = "as_list"
    AS_INT = "as_int"
    AS_FLOAT = "as_float"
    AS_STRING = "as_string"
    AS_BOOL = "as_bool"
    AS_NONE = "as_none"
    # AS_CUSTOM1 = "as_custom1"
    # AS_CUSTOM2 = "as_custom2"


class Deconstructor(BaseDeconstructor[T_interm]):
    """Default concrete deconstructor"""

    def deconstruct(self, obj: Any) -> T_interm: ...
