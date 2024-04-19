# SPDX-License-Identifier: BSD-3-Clause

from xattrs._compat.typing import Any, AnyStr, Callable, TypeVar

from datetime import datetime
from enum import Enum
from json import dumps as _dumps
from json import loads as _loads

from xattrs.abc import AbstractDeserializer, AbstractSerializer
from xattrs.constructor import Constructor
from xattrs.deconstructor import Deconstructor
from xattrs.deserializer import Deserializer
from xattrs.serializer import Serializer

__all__ = ["from_json", "to_json"]

# Supports the following objects and types by default:
#
# +-------------------+---------------+
# | Python            | JSON          |
# +===================+===============+
# | dict              | object        |
# +-------------------+---------------+
# | list, tuple       | array         |
# +-------------------+---------------+
# | str               | string        |
# +-------------------+---------------+
# | int, float        | number        |
# +-------------------+---------------+
# | True              | true          |
# +-------------------+---------------+
# | False             | false         |
# +-------------------+---------------+
# | None              | null          |
# +-------------------+---------------+
#

T = TypeVar("T")

T_json = TypeVar("T_json", dict, list, tuple, str, int, float, bool, None)


class JsonValue(Enum):
    """JSON value."""

    Object = dict
    Array = tuple | list
    String = str
    Number = int | float
    TRUE = True
    FALSE = False
    Null = None


class JsonDeconstructor(Deconstructor[T_json]):
    """JSON constructor."""

    def _datetime_to_isoformat(self, value: datetime) -> str:
        """Convert the value to an intermediate data types."""
        raise value.isoformat()


class JsonConstructor(Constructor[T_json]):
    """JSON decoder."""

    def _datetime_from_isoformat(self, value: str) -> datetime:
        """Convert the value to a Python object."""
        return datetime.fromisoformat(value)


class JsonDeserializer(Deserializer[AnyStr, T_json]):
    """JSON deserializer."""

    def decode(self, data: AnyStr, **kwargs) -> T_json:
        """Deserialize the JSON string to an object."""
        return _loads(data)


class JsonSerializer(Serializer[T_json, str]):
    """JSON serializer."""

    def encode(self, obj: T_json, **kwargs) -> str:
        """Serialize the object to a JSON-formatted string."""
        return _dumps(obj)


default_json_serializer = JsonSerializer()
default_json_deserializer = JsonDeserializer()


def from_json(
    s: AnyStr,
    cls: type[T],
    *,
    deserializer: AbstractDeserializer[AnyStr, T_json] | None = None,
    **kw,
) -> T:
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.
    """
    deserializer = deserializer or default_json_deserializer
    loads = deserializer.loads
    return loads(s, cls, **kw)


def to_json(
    obj: Any,
    *,
    serializer: AbstractSerializer[T_json, str] | Callable[..., str] | None = None,
    **kw,
) -> str:
    """Serialize ``obj`` to a JSON-formatted ``str``."""
    if serializer is None:
        dumps = default_json_serializer.dumps
    elif isinstance(serializer, AbstractSerializer):
        dumps = serializer.dumps
    else:
        dumps = serializer
    return dumps(obj, **kw)
