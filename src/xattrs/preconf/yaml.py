# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import types
from xattrs._compat.typing import Any, AnyStr, Callable, TypeVar, Union

from datetime import datetime
from functools import partial
from io import StringIO

from ruamel.yaml import YAML

from xattrs._struct_funcs import asdict_shallow
from xattrs.deserializer import Deserializer
from xattrs.serializer import Serializer
from xattrs.typing import CaseConvention, DeserializeFunc, SerializeFunc

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


def _yaml_dumps(obj: Any, *, _ruamel_yaml: YAML, **kwargs: Any) -> str:
    """Serialize ``obj`` to a JSON-formatted ``str``."""
    with StringIO() as stream:
        _ruamel_yaml.dump(obj, stream, **kwargs)
        return stream.getvalue()


def _yaml_loads(obj: str, *, _ruamel_yaml: YAML, **kwargs: Any) -> str:
    """Serialize ``obj`` to a JSON-formatted ``str``."""
    with StringIO() as stream:
        stream.write(obj)
        data = _ruamel_yaml.load(stream, **kwargs)
        return data


class YamlDeserializer(Deserializer):
    """JSON deserializer."""

    def __init__(self, loads: Callable | None = None):
        if loads is None:
            _yaml = YAML(typ="safe")
            _yaml.default_flow_style = False

            self._loads = partial(_yaml_loads, _ruamel_yaml=_yaml)
        else:
            self._loads = loads

    # @Deserializer.dispatch(datetime)
    def _datetime_from_isoformat(self, value: str, **kw) -> datetime:
        """Convert the value to a Python object."""
        return datetime.fromisoformat(value)

    def loads(self, s: AnyStr, **kw) -> Any: ...
    def load(self, fp: Any, **kw) -> Any: ...

    def from_yaml(
        self,
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
        loads = loads or self.loads
        return loads(fromdict(s, cls), **kw)


class YamlSerializer(Serializer):
    """YAML serializer."""

    def __init__(
        self,
        case: CaseConvention | None = None,
        exclude_if_default: bool = False,
        global_filter: None = None,
        dumps: Callable | None = None,
    ):
        if dumps is None:
            _yaml = YAML(typ="safe")
            _yaml.default_flow_style = False
            self._dumps = partial(_yaml_dumps, _ruamel_yaml=_yaml)
        else:
            self._dumps = dumps

    # @Serializer.dispatch(datetime)
    def _datetime_to_isoformat(self, value: datetime, **kw) -> str:
        """Convert the value to an intermediate data types."""
        return value.isoformat()

    def dumps(self, obj: Any, **kw) -> str: ...
    def dump(self, obj: Any, fp: Any, **kw) -> None: ...

    def to_yaml(
        self,
        obj: Any,
        *,
        key_serializer: Callable[[str], str] | None = None,
        value_serializer: SerializeFunc | None = None,
        dumps: Callable | None = None,
        **kwargs: Any,
    ) -> str:
        """Serialize ``obj`` to a JSON-formatted ``str``."""
        value_serializer = value_serializer or default_yaml_serializer
        dumps = dumps or self._dumps
        return dumps(
            asdict_shallow(
                obj, key_serializer=key_serializer, value_serializer=value_serializer
            ),
            **kwargs,
        )


default_yaml_serializer = YamlSerializer()
default_yaml_deserializer = YamlDeserializer()

to_yaml = default_yaml_serializer.to_yaml
from_yaml = default_yaml_deserializer.from_yaml
dumps = default_yaml_serializer.dumps
loads = default_yaml_deserializer.loads
dump = default_yaml_serializer.dump
load = default_yaml_deserializer.load
