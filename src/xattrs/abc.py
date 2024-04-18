from __future__ import annotations

from xattrs._compat.typing import Any, Callable, Generic

from abc import ABC, abstractmethod

from xattrs.typing import A, B, ConstructHook, DeconstructHook, IntermType, T

###############################################################################


class AbstractConstructor(ABC, Generic[IntermType]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    _construct_hook_map: ...

    @abstractmethod
    def register_hook(self, Cls: type[Any], func: ConstructHook[Any]) -> None: ...

    @abstractmethod
    def construct(self, data: IntermType, Cls: type[Any]) -> Any: ...


class AbstractDeconstructor(ABC, Generic[IntermType]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def register_hook(self, Cls: type[Any], func: DeconstructHook[Any]) -> None: ...

    @abstractmethod
    def deconstruct(self, obj: Any) -> IntermType: ..


class AbstractConverter(ABC, Generic[IntermType]):
    constructor: AbstractConstructor[IntermType]
    deconstrucor: AbstractDeconstructor[IntermType]

    @abstractmethod
    def register_construct_hook(
        self, Cls: type[Any], func: ConstructHook[Any]
    ) -> None: ...

    @abstractmethod
    def register_deconstruct_hook(
        self, Cls: type[Any], func: DeconstructHook[Any]
    ) -> None: ...


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
    def encode(self, obj: IntermType, **kwargs) -> T: ...

    @abstractmethod
    def deconstruct(self, obj: Any, **kwargs) -> IntermType: ...

    @abstractmethod
    def dumps(self, obj: Any, **kwargs) -> T: ...


class AbstractDeserializer(ABC, Generic[T, IntermType]):
    constructor: AbstractConstructor[IntermType]
    decoder: AbstractDecoder[T, IntermType]

    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def decode(self, data: T, **kwargs) -> IntermType: ...

    @abstractmethod
    def construct(self, data: IntermType, obj: type[Any], **kwargs) -> Any: ...

    @abstractmethod
    def loads(self, data: T, obj: type[Any], **kwargs) -> Any: ...


class AbstractSerDe(ABC, Generic[IntermType, A, B]):
    deserializer: AbstractDeserializer[A, IntermType]
    serializer: AbstractSerializer[IntermType, B]

    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def loads(self, data: A, obj: type[Any], **kwargs) -> Any: ...

    @abstractmethod
    def decode(self, data: A, **kwargs) -> IntermType: ...

    @abstractmethod
    def construct(self, data: IntermType, obj: type[Any], **kwargs) -> Any: ...

    @abstractmethod
    def deconstruct(self, obj: Any) -> IntermType: ...

    @abstractmethod
    def encode(self, obj: IntermType, **kwargs) -> B: ...

    @abstractmethod
    def dumps(self, obj: Any, **kwargs) -> B: ...
