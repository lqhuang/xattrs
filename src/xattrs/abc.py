# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs._compat.typing import Callable, Generic

from abc import ABC, abstractmethod

from xattrs.typing import (
    ConstructHook,
    DeconstructHook,
    K,
    T,
    T_co,
    T_contra,
    T_dpcallable,
    T_interm,
    T_pred,
    T_proto,
    T_pyobj,
)

###############################################################################


class AbstractConstructor(ABC, Generic[T_interm]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    _construct_hook_map: ...

    @abstractmethod
    def register_hook(
        self, cls: type[T_pyobj], func: ConstructHook[T_pyobj, T_interm]
    ) -> None: ...

    @abstractmethod
    def construct(self, data: T_interm, cls: type[T_pyobj]) -> T_pyobj: ...


class AbstractDeconstructor(ABC, Generic[T_interm]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def register_hook(
        self, cls: type[T_pyobj], func: DeconstructHook[T_pyobj, T_interm]
    ) -> None: ...

    @abstractmethod
    def deconstruct(self, obj: T_pyobj) -> T_interm: ...


class AbstractConverter(ABC, Generic[T_interm]):
    constructor: AbstractConstructor[T_interm]
    deconstrucor: AbstractDeconstructor[T_interm]

    @abstractmethod
    def register_construct_hook(
        self, cls: type[T_pyobj], func: ConstructHook[T_pyobj, T_interm]
    ) -> None: ...

    @abstractmethod
    def register_deconstruct_hook(
        self, cls: type[T_pyobj], func: DeconstructHook[T_pyobj, T_interm]
    ) -> None: ...


###############################################################################


class AbstractCodec(ABC, Generic[T_contra, T_co, T_proto]):
    encoder: AbstractEncoder[T_contra, T_proto]
    decoder: AbstractDecoder[T_proto, T_co]


class AbstractEncoder(ABC, Generic[T_contra, T_proto]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def encode(self, data: T_contra) -> T_proto: ...


class AbstractDecoder(ABC, Generic[T_proto, T_co]):
    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def decode(self, data: T_proto, **kwargs) -> T_co: ...


###############################################################################


class AbstractSerializer(ABC, Generic[T_contra, T_proto]):
    deconstructor: AbstractDeconstructor[T_contra]
    encoder: AbstractEncoder[T_contra, T_proto]

    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def encode(self, obj: T_contra, **kwargs) -> T_proto: ...

    @abstractmethod
    def deconstruct(self, obj: T_pyobj, **kwargs) -> T_contra: ...

    @abstractmethod
    def dumps(self, obj: T_pyobj, **kwargs) -> T_proto: ...


class AbstractDeserializer(ABC, Generic[T_proto, T_co]):
    constructor: AbstractConstructor[T_co]
    decoder: AbstractDecoder[T_proto, T_co]

    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def decode(self, data: T_proto, **kwargs) -> T_co: ...

    @abstractmethod
    def construct(self, data: T_co, obj: type[T_pyobj], **kwargs) -> T_pyobj: ...

    @abstractmethod
    def loads(self, data: T_proto, obj: type[T_pyobj], **kwargs) -> T_pyobj: ...


class AbstractSerDe(ABC, Generic[T_contra, T_co, T_proto]):
    serializer: AbstractSerializer[T_contra, T_proto]
    deserializer: AbstractDeserializer[T_proto, T_co]

    def __call__(self, wrapped: T) -> Callable[[T], T]: ...

    @abstractmethod
    def loads(self, data: T_proto, obj: type[T_pyobj], **kwargs) -> T_pyobj: ...

    @abstractmethod
    def decode(self, data: T_proto, **kwargs) -> T_co: ...

    @abstractmethod
    def construct(self, data: T_co, obj: type[T_pyobj], **kwargs) -> T_pyobj: ...

    @abstractmethod
    def deconstruct(self, obj: T_pyobj) -> T_contra: ...

    @abstractmethod
    def encode(self, obj: T_contra, **kwargs) -> T_proto: ...

    @abstractmethod
    def dumps(self, obj: T_pyobj, **kwargs) -> T_proto: ...


###############################################################################


class AbstractDispatcher(ABC, Generic[T_dpcallable]):

    @abstractmethod
    def dispatch(self, cls: type[T]) -> T_dpcallable: ...

    @abstractmethod
    def register(self, cls: type[K], func: T_dpcallable) -> T_dpcallable: ...


class AbstractPredicateDispatcher(ABC, Generic[T_pred, T_dpcallable]):

    @abstractmethod
    def dispatch(self, pred: T_pred) -> T_dpcallable: ...

    @abstractmethod
    def register(self, cls: T_pred, func: T_dpcallable) -> T_dpcallable: ...
