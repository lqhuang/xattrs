# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import types
from xattrs._compat.typing import Any, AnyStr, Callable, TypeVar, Union

from datetime import datetime
from io import StringIO

from ruamel.yaml import YAML

from xattrs._struct_funcs import _shallow_asdict
from xattrs.deserializer import Deserializer
from xattrs.serializer import Serializer
from xattrs.typing import DeserializeFunc, SerializeFunc

__all__ = ("from_yaml", "to_yaml", "dumps", "loads", "dump", "load")

# Supports the following objects and types by default:
#
# +-------------------+---------------+
# | Python            | Yaml          |
# +===================+===============+
# | dict              | map           |
# +-------------------+---------------+
# | list, tuple       | seq           |
# +-------------------+---------------+
# | str               | string        |
# +-------------------+---------------+
# | int               | int           |
# +-------------------+---------------+
# | float             | float         |
# +-------------------+---------------+
# | True              | true          |
# +-------------------+---------------+
# | False             | false         |
# +-------------------+---------------+
# | None              | null          |
# +-------------------+---------------+
#

T = TypeVar("T")

Yaml = Union[dict, list, tuple, str, int, float, bool, types.NoneType]  # type: ignore[type-arg]


class YamlDeserializer(Deserializer):
    """JSON deserializer."""

    # @Deserializer.dispatch(datetime)
    def _datetime_from_isoformat(self, value: str, **kw) -> datetime:
        """Convert the value to a Python object."""
        return datetime.fromisoformat(value)


class YamlSerializer(Serializer):
    """JSON serializer."""

    # @Serializer.dispatch(datetime)
    def _datetime_to_isoformat(self, value: datetime, **kw) -> str:
        """Convert the value to an intermediate data types."""
        return value.isoformat()


_yaml = YAML(typ="safe")  # default, if not specfied, is 'rt' (round-trip)
# _yaml.indent(mapping=2, sequence=2, offset=0) # default
_yaml.default_flow_style = False
default_yaml_serializer = YamlSerializer()
default_yaml_deserializer = YamlDeserializer()


def from_yaml(
    s: AnyStr,
    cls: type[T],
    *,
    deserializer: DeserializeFunc | None = None,
    loads: Callable | None = None,
    **kw,
) -> T:
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.
    """
    deserializer = deserializer or default_yaml_deserializer
    loads = loads or _yaml.load
    return loads(fromdict(s, cls), **kw)


def _yaml_dumps(obj: Any, **kwargs: Any) -> str:
    """Serialize ``obj`` to a JSON-formatted ``str``."""
    with StringIO() as stream:
        _yaml.dump(obj, stream, **kwargs)
        return stream.getvalue()


def to_yaml(
    obj: Any,
    *,
    key_serializer: Callable[[str], str] | None = None,
    value_serializer: SerializeFunc | None = None,
    dumps: Callable | None = None,
    **kwargs: Any,
) -> str:
    """Serialize ``obj`` to a JSON-formatted ``str``."""
    value_serializer = value_serializer or default_yaml_serializer
    dumps = dumps or _yaml_dumps
    return dumps(
        _shallow_asdict(
            obj, key_serializer=key_serializer, value_serializer=value_serializer
        ),
        **kwargs,
    )
