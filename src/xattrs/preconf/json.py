# SPDX-License-Identifier: BSD-3-Clause

from xattrs._compat.typing import (
    Any,
    AnyStr,
    Callable,
    Concatenate,
    Optional,
    TypeVar,
    Union,
)

from datetime import datetime
from json import dumps as _dumps
from json import loads as _loads

from xattrs.abc import AbstractDeserializer, AbstractSerializer
from xattrs.constructor import Constructor
from xattrs.deconstructor import Deconstructor
from xattrs.deserializer import Deserializer
from xattrs.serializer import Serializer
from xattrs.typing import P

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

Json = Union[dict, list, tuple, str, int, float, bool, None]  # type: ignore[type-arg]


class JsonDeconstructor(Deconstructor[Json]):
    """JSON constructor."""

    def _datetime_to_isoformat(self, value: datetime) -> str:
        """Convert the value to an intermediate data types."""
        return value.isoformat()


class JsonConstructor(Constructor[Json]):
    """JSON decoder."""

    def _datetime_from_isoformat(self, value: str) -> datetime:
        """Convert the value to a Python object."""
        return datetime.fromisoformat(value)


class JsonDeserializer(Deserializer[AnyStr, Json]):
    """JSON deserializer."""

    def decode(self, data: AnyStr, **kwargs: Any) -> Any:
        """Deserialize the JSON string to an object."""
        return _loads(data)


class JsonSerializer(Serializer[Json, str]):
    """JSON serializer."""

    def encode(self, obj: Json, **kwargs: Any) -> str:
        """Serialize the object to a JSON-formatted string."""
        return _dumps(obj)


default_json_serializer = JsonSerializer()
default_json_deserializer = JsonDeserializer()


def from_json(
    s: AnyStr,
    cls: type[T],
    *,
    deserializer: Optional[AbstractDeserializer[AnyStr, Json]] = None,
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
    serializer: Union[
        AbstractSerializer[Json, str], Callable[Concatenate[Json, P], str], None
    ] = None,
    **kwargs: Any,
) -> str:
    """Serialize ``obj`` to a JSON-formatted ``str``."""
    if serializer is None:
        dumps = default_json_serializer.dumps
    elif isinstance(serializer, AbstractSerializer):
        dumps = serializer.dumps
    else:
        dumps = serializer
    return dumps(obj, **kwargs)
