# SPDX-License-Identifier: MIT
from __future__ import annotations

from xattrs._compat.typing import TYPE_CHECKING, Any
from xattrs._typing import T, T_interm, T_proto

from xattrs.abc import AbstractDeserializer, AbstractSerDe, AbstractSerializer

if TYPE_CHECKING:
    from xattrs._typing import ConstructHook, DeconstructHook, Dispatchable


class BaseSerializer(AbstractSerializer[T_interm, T_proto]):
    """Base serializer."""

    def _dumps(self, obj: Any, **kwargs) -> T_proto:
        return self.encode(self.deconstruct(obj, **kwargs), **kwargs)


class BaseDeserializer(AbstractDeserializer[T_proto, T_interm]):
    """Base deserializer."""

    def decode(self, data: T_proto, **kwargs) -> T_interm:
        raise NotImplementedError

    def construct(self, data: T_interm, obj: type[T], **kwargs) -> T:
        raise NotImplementedError

    def loads(self, data: T_proto, obj: type[T], **kwargs) -> T:
        return self.construct(self.decode(data, **kwargs), obj)


class BaseSerDe(AbstractSerDe[T_interm, T_interm, T_proto]):
    """Base serializer/deserializer."""

    serializer: BaseSerializer[T_interm, T_proto]
    deserializer: BaseDeserializer[T_proto, T_interm]

    def loads(
        self, data: T_proto, obj: type[T], **kwargs
    ) -> T:  # pyright: ignore[reportReturnType]
        self.deserializer.loads(data, obj, **kwargs)

    def dumps(self, obj: Any, **kwargs) -> T_proto:  # pyright: ignore[reportReturnType]
        self.serializer.dumps(obj, **kwargs)
