from __future__ import annotations

from xattrs._compat.typing import Any

from xattrs.abc import (
    AbstractConstructor,
    AbstractConverter,
    AbstractDeconstructor,
    AbstractDeserializer,
    AbstractSerDe,
    AbstractSerializer,
)
from xattrs.typing import A, B, ConstructHook, DeconstructHook, IntermType, T


class BaseConstructor(AbstractConstructor[IntermType]):
    """Base constructor."""

    def construct(self, data: IntermType, Cls: type[Any]) -> Any:
        raise NotImplementedError


class BaseDeconstructor(AbstractDeconstructor[IntermType]):
    """Base deconstructor."""

    def deconstruct(self, obj: Any) -> IntermType:
        raise NotImplementedError


### Using `singledispatch` has a problem, it's difficult to mix in...
# How can I mix in a class that already register a few methods of `singledispatch`?


class BaseConverter(AbstractConverter[IntermType]):
    """Base converter."""

    def construct(self, data: IntermType, Cls: type[Any]) -> Any:
        raise NotImplementedError

    def deconstruct(self, obj: Any) -> IntermType:
        raise NotImplementedError

    def register_construct_hook(self, Cls: type[Any], func: ConstructHook[Any]) -> None:
        raise NotImplementedError

    def register_deconstruct_hook(
        self, Cls: type[Any], func: DeconstructHook[Any]
    ) -> None:
        raise NotImplementedError


#
#
#


class BaseSerializer(AbstractSerializer[IntermType, T]):
    """Base serializer."""

    def deconstruct(self, obj: Any, **kwargs) -> IntermType:
        raise NotImplementedError

    def encode(self, obj: IntermType, **kwargs) -> T:
        raise NotImplementedError

    def dumps(self, obj: Any, **kwargs) -> T:
        self.encode(self.deconstruct(obj, **kwargs), **kwargs)


class BaseDeserializer(AbstractDeserializer[T, IntermType]):
    """Base deserializer."""

    constructor: BaseConstructor[IntermType]

    def decode(self, data: T, **kwargs) -> IntermType:
        raise NotImplementedError

    def construct(self, data: IntermType, obj: type[Any], **kwargs) -> Any:
        raise NotImplementedError

    def loads(self, data: T, obj: type[Any], **kwargs) -> Any:
        self.construct(self.decode(data, **kwargs), obj)


class BaseSerDe(AbstractSerDe[IntermType, A, B]):
    deserializer: BaseDeserializer[A, IntermType]
    serializer: BaseSerializer[IntermType, B]

    def loads(self, data: A, obj: type[Any], **kwargs) -> Any:
        self.deserializer.loads(data, obj, **kwargs)

    def dumps(self, obj: Any, **kwargs) -> B:
        self.serializer.dumps(obj, **kwargs)
