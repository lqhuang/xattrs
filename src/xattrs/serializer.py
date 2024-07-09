# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Callable
from xattrs._typing import AttrsInstance, DataclassInstance, T_interm, T_proto


from xattrs._helpers import _identity
from xattrs._serde import _get_serde
from xattrs.base import BaseSerializer
from xattrs.converters import _CASE_CONVERTER_MAPPING


class Serializer(BaseSerializer[T_interm, T_proto]): ...


_KeySerializer = Callable
_ValueSerializer = Callable
