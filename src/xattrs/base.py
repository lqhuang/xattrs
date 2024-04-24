# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import TYPE_CHECKING, Any

from xattrs.abc import (
    AbstractConstructor,
    AbstractConverter,
    AbstractDeconstructor,
    AbstractDeserializer,
    AbstractSerDe,
    AbstractSerializer,
)
from xattrs.typing import T, T_interm, T_proto

if TYPE_CHECKING:
    from xattrs.typing import ConstructHook, DeconstructHook, Dispatchable


class BaseConstructor(AbstractConstructor[T_interm]):
    """Base constructor."""

    def construct(self, data: T_interm, cls: type[T]) -> T:
        raise NotImplementedError


class BaseDeconstructor(AbstractDeconstructor[T_interm]):
    """Base deconstructor."""

    def deconstruct(self, obj: T) -> T_interm:
        raise NotImplementedError


### Using `singledispatch` has a problem, it's difficult to mix in...
# How can I mix in a class that already register a few methods of `singledispatch`?


class BaseConverter(AbstractConverter[T_interm]):
    """Base converter."""

    def construct(self, data: T_interm, cls: type[T]) -> T:
        raise NotImplementedError

    def deconstruct(self, obj: T) -> T_interm:
        raise NotImplementedError

    def register_construct_hook(
        self, cls: type[T], func: ConstructHook[T, T_interm]
    ) -> None:
        raise NotImplementedError

    def register_deconstruct_hook(self, cls: type[T], func: DeconstructHook[T]) -> None:
        raise NotImplementedError


#
#
#


class BaseSerializer(AbstractSerializer[T_interm, T_proto]):
    """Base serializer."""

    def deconstruct(self, obj: Any, **kwargs) -> T_interm:
        raise NotImplementedError

    def encode(self, obj: T_interm, **kwargs) -> T_proto:
        raise NotImplementedError

    def dumps(self, obj: Any, **kwargs) -> T_proto:
        return self.encode(self.deconstruct(obj, **kwargs), **kwargs)


class BaseDeserializer(AbstractDeserializer[T_proto, T_interm]):
    """Base deserializer."""

    constructor: BaseConstructor[T_interm]

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
