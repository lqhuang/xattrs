# SPDX-License-Identifier: BSD-3-Clause

from typing import Any, AnyStr, TypeVar

from enum import Enum
from json import dumps, loads

from xattrs.abc import (
    AbstractDecoder,
    AbstractDeserializer,
    AbstractEncoder,
    AbstractSerializer,
)
from xattrs.typing import XattrsInstance

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

JsonPri = TypeVar("JsonPri", dict, list, tuple, str, int, float, bool, None)


class JsonValue(Enum):
    """JSON value."""

    Object = dict
    Array = tuple | list
    String = str
    Number = int | float
    TRUE = True
    FALSE = False
    Null = None


class JsonEncoder(AbstractEncoder[str]):
    """JSON encoder."""

    def __call__(self, value: Any) -> str:
        """Encode the value to a JSON-compatible format."""
        return dumps(value)


class JsonDecoder(AbstractDecoder[AnyStr]):
    """JSON decoder."""

    def decode(self, value: Any) -> Any:
        """Decode the JSON-compatible value to the original format."""
        return value


# Instance
# or
# Class
#
# required features:
#
# 1. Easy to customize
# 2. Easy to extend
# 3. be able to use in multiple threads / multiple processes
# 4. be able to transform to another machine (remote) / reference tranparency
# 5. immutable?
#


class JsonDeserializer(AbstractDeserializer[AnyStr]):
    """JSON deserializer."""

    def __call__(
        self, data: AnyStr, obj: type[XattrsInstance], **kwargs
    ) -> XattrsInstance:
        """Deserialize the JSON string to an object."""
        return loads(data)


class JsonSerializer(AbstractSerializer[str]):
    """JSON serializer."""

    def __call__(self, obj: Any, **kwargs) -> str:
        """Serialize the object to a JSON string."""
        return dumps(obj)


default_json_serializer = JsonDeserializer()


def from_json(
    s: AnyStr,
    obj: type[T],
    *,
    deserializer: AbstractDeserializer[AnyStr] | None = None,
    **kw,
) -> T:
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.
    """
    de = deserializer or default_json_serializer
    return de(s, obj, **kw)


def to_json(
    obj: Any,
    *,
    serializer: AbstractSerializer[AnyStr] | None = None,
    **kw,
) -> AnyStr:
    """Serialize ``obj`` to a JSON-formatted ``str``."""
    se = serializer or default_json_serializer
    return se(obj, **kw)
