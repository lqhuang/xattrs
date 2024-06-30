# SPDX-License-Identifier: BSD-3-Clause
# mypy: disable-error-code="empty-body"
from __future__ import annotations

from types import MappingProxyType
from xattrs._compat.typing import TYPE_CHECKING, Any, Callable, Generic

from abc import abstractmethod

from xattrs.typing import SingleDispatchCallable, T, T_co, T_contra, T_interm, T_proto

if TYPE_CHECKING:
    from xattrs.typing import ConstructHook, DeconstructHook, Dispatchable

###############################################################################


class AbstractConstructor(Generic[T_interm]):
    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def register_hook(
        self, cls: Dispatchable[T], func: ConstructHook[T, T_interm]
    ) -> ConstructHook[T, T_interm]: ...

    @abstractmethod
    def construct(
        self, cls: type[T], data: T_interm, *arg: Any, **kwargs: Any
    ) -> T: ...


class AbstractDeconstructor(Generic[T_interm]):
    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def register_hook(
        self, cls: Dispatchable[T], func: DeconstructHook[T_interm]
    ) -> DeconstructHook[T_interm]: ...

    @abstractmethod
    def deconstruct(self, obj: Any, *arg: Any, **kwargs: Any) -> T_interm: ...


class AbstractConverter(Generic[T_interm]):
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


class AbstractEncoder(Generic[T_contra, T_proto]):
    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def encode(self, data: T_contra, *arg: Any, **kwargs: Any) -> T_proto: ...


class AbstractDecoder(Generic[T_proto, T_co]):
    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def decode(self, data: T_proto, *arg: Any, **kwargs: Any) -> T_co: ...


class AbstractCodec(Generic[T_contra, T_co, T_proto]):
    encoder: AbstractEncoder[T_contra, T_proto]
    decoder: AbstractDecoder[T_proto, T_co]


###############################################################################


class AbstractSerializer(Generic[T_contra, T_proto]):
    deconstructor: AbstractDeconstructor[T_contra]
    encoder: AbstractEncoder[T_contra, T_proto]

    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def encode(self, obj: T_contra, *arg: Any, **kwargs: Any) -> T_proto: ...

    @abstractmethod
    def deconstruct(self, obj: Any, *arg: Any, **kwargs: Any) -> T_contra: ...  # type: ignore[misc]

    @abstractmethod
    def dumps(self, obj: Any, *arg: Any, **kwargs: Any) -> T_proto: ...


class AbstractDeserializer(Generic[T_proto, T_co]):
    constructor: AbstractConstructor[T_co]
    decoder: AbstractDecoder[T_proto, T_co]

    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def decode(self, data: T_proto, *arg: Any, **kwargs: Any) -> T_co: ...

    @abstractmethod
    def construct(self, data: T_co, obj: type[T], *arg: Any, **kwargs: Any) -> T: ...  # type: ignore[misc]

    @abstractmethod
    def loads(self, data: T_proto, obj: type[T], *arg: Any, **kwargs: Any) -> T: ...


class AbstractSerDe(Generic[T_contra, T_co, T_proto]):
    serializer: AbstractSerializer[T_contra, T_proto]
    deserializer: AbstractDeserializer[T_proto, T_co]

    def __call__(self, wrapped: T) -> T: ...

    @abstractmethod
    def loads(self, data: T_proto, obj: type[T], *arg: Any, **kwargs: Any) -> T: ...

    @abstractmethod
    def decode(self, data: T_proto, *arg: Any, **kwargs: Any) -> T_co: ...

    @abstractmethod
    def construct(self, data: T_co, obj: type[T], *arg: Any, **kwargs: Any) -> T: ...  # type: ignore[misc]

    @abstractmethod
    def deconstruct(self, obj: Any, *arg: Any, **kwargs: Any) -> T_contra: ...  # type: ignore[misc]

    @abstractmethod
    def encode(self, obj: T_contra, *arg: Any, **kwargs: Any) -> T_proto: ...

    @abstractmethod
    def dumps(self, obj: Any, *arg: Any, **kwargs: Any) -> T_proto: ...


###############################################################################


class AbstractDispatcher(Generic[T]):
    _registry: MappingProxyType[str, SingleDispatchCallable[T]]

    @abstractmethod
    def dispatch(self, cls: Dispatchable[T]) -> Callable[..., T]: ...

    @abstractmethod
    def register(
        self, cls: Dispatchable[T], func: Callable[..., T]
    ) -> Callable[..., T]: ...
