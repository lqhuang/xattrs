# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from types import MappingProxyType
from xattrs._compat.typing import TYPE_CHECKING, Any, Callable, Generic

from abc import ABC, abstractmethod

from xattrs.typing import SingleDispatchCallable, T, T_co, T_contra, T_interm, T_proto

if TYPE_CHECKING:
    from xattrs.typing import ConstructHook, DeconstructHook, Dispatchable

###############################################################################


class AbstractConstructor(ABC, Generic[T_interm]):
    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def register_hook(
        self, cls: Dispatchable[T], func: ConstructHook[T, T_interm]
    ) -> ConstructHook[T, T_interm]: ...

    @abstractmethod
    def construct(self, cls: type[T], data: T_interm, *arg, **kwargs) -> T: ...


class AbstractDeconstructor(ABC, Generic[T_interm]):
    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def register_hook(
        self, cls: Dispatchable[T], func: DeconstructHook[T_interm]
    ) -> DeconstructHook[T_interm]: ...

    @abstractmethod
    def deconstruct(self, obj: Any, *arg, **kwargs) -> T_interm: ...


class AbstractConverter(ABC, Generic[T_interm]):
    constructor: AbstractConstructor[T_interm]
    deconstrucor: AbstractDeconstructor[T_interm]

    @abstractmethod
    def register_construct_hook(
        self, cls: type[T], func: ConstructHook[T, T_interm]
    ) -> ConstructHook[T, T_interm]: ...

    @abstractmethod
    def register_deconstruct_hook(
        self, cls: type[T], func: DeconstructHook[T_interm]
    ) -> DeconstructHook[T_interm]: ...


###############################################################################


class AbstractEncoder(ABC, Generic[T_contra, T_proto]):
    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def encode(self, data: T_contra, *arg, **kwargs) -> T_proto: ...


class AbstractDecoder(ABC, Generic[T_proto, T_co]):
    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def decode(self, data: T_proto, *arg, **kwargs) -> T_co: ...


class AbstractCodec(ABC, Generic[T_contra, T_co, T_proto]):
    encoder: AbstractEncoder[T_contra, T_proto]
    decoder: AbstractDecoder[T_proto, T_co]


###############################################################################


class AbstractSerializer(ABC, Generic[T_contra, T_proto]):
    deconstructor: AbstractDeconstructor[T_contra]
    encoder: AbstractEncoder[T_contra, T_proto]

    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def encode(self, obj: T_contra, *arg, **kwargs) -> T_proto: ...

    @abstractmethod
    def deconstruct(self, obj: Any, *arg, **kwargs) -> T_contra: ...

    @abstractmethod
    def dumps(self, obj: Any, *arg, **kwargs) -> T_proto: ...


class AbstractDeserializer(ABC, Generic[T_proto, T_co]):
    constructor: AbstractConstructor[T_co]
    decoder: AbstractDecoder[T_proto, T_co]

    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def decode(self, data: T_proto, *arg, **kwargs) -> T_co: ...

    @abstractmethod
    def construct(self, data: T_co, obj: type[T], *arg, **kwargs) -> T: ...

    @abstractmethod
    def loads(self, data: T_proto, obj: type[T], *arg, **kwargs) -> T: ...


class AbstractSerDe(ABC, Generic[T_contra, T_co, T_proto]):
    serializer: AbstractSerializer[T_contra, T_proto]
    deserializer: AbstractDeserializer[T_proto, T_co]

    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def loads(self, data: T_proto, obj: type[T], *arg, **kwargs) -> T: ...

    @abstractmethod
    def decode(self, data: T_proto, *arg, **kwargs) -> T_co: ...

    @abstractmethod
    def construct(self, data: T_co, obj: type[T], *arg, **kwargs) -> T: ...

    @abstractmethod
    def deconstruct(self, obj: Any, *arg, **kwargs) -> T_contra: ...

    @abstractmethod
    def encode(self, obj: T_contra, *arg, **kwargs) -> T_proto: ...

    @abstractmethod
    def dumps(self, obj: Any, *arg, **kwargs) -> T_proto: ...


###############################################################################


class AbstractDispatcher(ABC, Generic[T]):

    _registry: MappingProxyType[str, SingleDispatchCallable[T]]

    @abstractmethod
    def dispatch(self, cls: Dispatchable[T]) -> Callable[..., T]: ...

    @abstractmethod
    def register(
        self, cls: Dispatchable[T], func: Callable[..., T]
    ) -> Callable[..., T]: ...
