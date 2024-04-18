from __future__ import annotations

from xattrs._compat.typing import Any, Callable, Generic

from abc import ABC, abstractmethod

from xattrs.typing import A, B, ConstructHook, DeconstructHook, IntermType, T

###############################################################################


class AbstractConverter(ABC, Generic[IntermType]):
    constructor: AbstractConstructor[IntermType]
    deconstrucor: AbstractDeconstructor[IntermType]


class AbstractConstructor(ABC, Generic[IntermType]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def register_hook(self, Cls: type[Any], func: ConstructHook[Any]) -> Any: ...

    @abstractmethod
    def from_interm(self, data: IntermType, Cls: type[Any]) -> Any: ...


class AbstractDeconstructor(ABC, Generic[IntermType]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def register_hook(
        self, Cls: type[Any], func: DeconstructHook[Any]
    ) -> IntermType: ...

    @abstractmethod
    def as_interm(self, obj: Any) -> IntermType: ...

    @abstractmethod
    def to(self, obj: Any) -> IntermType: ...


###############################################################################


class AbstractCodec(ABC, Generic[IntermType, A, B]):
    encoder: AbstractEncoder[IntermType, A]
    decoder: AbstractDecoder[B, IntermType]


class AbstractEncoder(ABC, Generic[IntermType, T]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def encode(self, data: IntermType) -> T: ...


class AbstractDecoder(ABC, Generic[T, IntermType]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def decode(self, data: T, **kwargs) -> IntermType: ...


###############################################################################


class AbstractSerializer(ABC, Generic[IntermType, T]):
    deconstructor: AbstractDeconstructor[IntermType]
    encoder: AbstractEncoder[IntermType, T]

    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def dumps(self, obj: Any, **kwargs) -> T:
        self.encoder.encode(self.deconstructor.as_interm(obj))


class AbstractDeserializer(ABC, Generic[T, IntermType]):
    constructor: AbstractConstructor[IntermType]
    decoder: AbstractDecoder[T, IntermType]

    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def loads(self, data: T, obj: type[Any], **kwargs) -> Any:
        self.constructor.from_interm(self.decoder.decode(data, **kwargs), obj)


class AbstractSerDe(ABC, Generic[IntermType, A, B]):
    deserializer: AbstractDeserializer[A, IntermType]
    serializer: AbstractSerializer[IntermType, B]

    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    def loads(self, data: A, obj: type[Any], **kwargs) -> Any:
        self.deserializer.loads(data, obj, **kwargs)

    @abstractmethod
    def _to(self, obj: Any) -> B: ...

    @abstractmethod
    def _from(self, data: B, **kwargs) -> IntermType: ...
