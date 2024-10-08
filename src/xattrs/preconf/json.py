# SPDX-License-Identifier: BSD-3-Clause

import types
from xattrs._compat.typing import Any, AnyStr, Callable, TypeVar, Union
from xattrs.typing import DeserializeFunc, SerializeFunc

import json
from datetime import datetime

from xattrs._struct_funcs import asdict_shallow
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

Jsonable = Union[dict, list, tuple, str, int, float, bool, types.NoneType]  # type: ignore[type-arg,valid-type]


class JsonDeserializer(Deserializer[AnyStr, Jsonable]):
    """JSON deserializer."""

    def _datetime_from_isoformat(self, value: str) -> datetime:
        """Convert the value to a Python object."""
        return datetime.fromisoformat(value)

    def loads(self, data: AnyStr, **kwargs: Any) -> Any:
        """Deserialize the JSON string to an object."""
        return json.loads(data)

    def from_json(
        self,
        s: AnyStr,
        cls: type[T],
        /,
        **kw,
    ) -> T:
        """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
        containing a JSON document) to a Python object.
        """
        # deserializer = deserializer or default_json_deserializer
        return json.loads(s, cls, **kw)


class JsonSerializer(Serializer[Jsonable, str]):
    """JSON serializer."""

    def _datetime_to_isoformat(self, value: datetime) -> str:
        """Convert the value to an intermediate data types."""
        return value.isoformat()

    def dumps(self, obj: Jsonable, **kwargs: Any) -> str:
        """Serialize the object to a JSON-formatted string."""
        return json.dumps(obj)

    def to_json(
        self,
        obj: Any,
        *,
        key_serializer: Callable[[str], str] | None = None,
        value_serializer: SerializeFunc | None = None,
        dumps: Callable | None = None,
        **kwargs: Any,
    ) -> str:
        """Serialize ``obj`` to a JSON-formatted ``str``."""
        value_serializer = value_serializer or self
        dumps = dumps or json.dumps
        return dumps(
            asdict_shallow(
                obj, key_serializer=key_serializer, value_serializer=value_serializer
            ),
            **kwargs,
        )


json_serializer = JsonSerializer()
json_deserializer = JsonDeserializer()

to_json = json_serializer.to_json
from_json = json_deserializer.from_json
dumps = json_serializer.dumps
loads = json_deserializer.loads
# dump = json_serializer.dump
# load = json_deserializer.load
