# SPDX-License-Identifier: MIT
from __future__ import annotations

import types
from xattrs._compat.typing import Any, AnyStr, Callable, TypeVar, Union
from xattrs.typing import CaseConvention, DeserializeFunc, SerializeFunc

from datetime import datetime
from functools import partial

from xattrs._struct_funcs import asdict_shallow
from xattrs.deserializer import Deserializer
from xattrs.serializer import Serializer

__all__ = ("dump", "dumps", "from_msgpack", "load", "loads", "to_msgpack")


MsgPackable = Union[dict, list, tuple, str, int, float, bool, types.NoneType]  # type: ignore[type-arg]


class MsgPackSerializer(Serializer[bytes, MsgPackable]): ...


class MsgPackDeserializer(Deserializer[bytes, MsgPackable]): ...
