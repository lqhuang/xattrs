# SPDX-License-Identifier: BSD-3-Clause

import types
from xattrs._compat.typing import Any, AnyStr, Callable, Optional, TypeVar, Union

from datetime import datetime
from json import dumps as _dumps
from json import loads as _loads

from xattrs._struct_funcs import _shallow_asdict
from xattrs.deserializer import Deserializer
from xattrs.serializer import Serializer
from xattrs.typing import DeserializeFunc, SerializeFunc

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

Json = Union[dict, list, tuple, str, int, float, bool, types.NoneType]  # type: ignore[type-arg]


class JsonDeserializer(Deserializer[AnyStr, Json]):
    """JSON deserializer."""

    def _datetime_from_isoformat(self, value: str) -> datetime:
        """Convert the value to a Python object."""
        return datetime.fromisoformat(value)

    def loads(self, data: AnyStr, **kwargs: Any) -> Any:
        """Deserialize the JSON string to an object."""
        return _loads(data)


class JsonSerializer(Serializer[Json, str]):
    """JSON serializer."""

    def _datetime_to_isoformat(self, value: datetime) -> str:
        """Convert the value to an intermediate data types."""
        return value.isoformat()

    def dumps(self, obj: Json, **kwargs: Any) -> str:
        """Serialize the object to a JSON-formatted string."""
        return _dumps(obj)


default_json_serializer = JsonSerializer()
default_json_deserializer = JsonDeserializer()


def from_json(
    s: AnyStr,
    cls: type[T],
    /,
    **kw,
) -> T:
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.
    """
    # deserializer = deserializer or default_json_deserializer
    return _loads(s, cls, **kw)


def to_json(
    obj: Any,
    *,
    key_serializer: Callable[[str], str] | None = None,
    value_serializer: SerializeFunc | None = None,
    dumps: Callable | None = None,
    **kwargs: Any,
) -> str:
    """Serialize ``obj`` to a JSON-formatted ``str``."""
    value_serializer = value_serializer or default_json_serializer
    dumps = dumps or _dumps
    return dumps(
        _shallow_asdict(
            obj, key_serializer=key_serializer, value_serializer=value_serializer
        ),
        **kwargs,
    )
