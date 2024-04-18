from __future__ import annotations

from typing import Any, Generic, TypeVar

from abc import ABC, abstractmethod

T = TypeVar("T")
IntermType = TypeVar("IntermType")  # interchange format / intermediary / bridge
PyObject = TypeVar("PyObject", Any)  # including dataclass, built-in types etc.


class AbstractSerDe(ABC, Generic[T]):
    deserialize: AbstractDeserializer[T]
    serialize: AbstractSerializer[T]

    @abstractmethod
    def _from(self, data: T) -> PyObject: ...

    @abstractmethod
    def _to(self, obj: PyObject) -> T: ...


class AbstractDeserializer(ABC, Generic[T]):
    @abstractmethod
    def __call__(self, data: T, obj: type[PyObject], **kwargs) -> PyObject: ...


class AbstractSerializer(ABC, Generic[T]):
    @abstractmethod
    def __call__(self, data: T) -> PyObject: ...


class AbstractConverter(ABC, Generic[IntermType, PyObject]):
    constructor: AbstractConstructor[IntermType, PyObject]
    deconstructor: AbstractDeconstructor[PyObject, IntermType]


class AbstractConstructor(ABC, Generic[IntermType, PyObject]):
    @abstractmethod
    def __call__(self, data: IntermType) -> PyObject:
        pass


class AbstractDeconstructor(ABC, Generic[PyObject, IntermType]):
    @abstractmethod
    def __call__(self, obj: PyObject) -> IntermType: ...


class AbstractEncoder(ABC, Generic[IntermType, T]):
    @abstractmethod
    def __call__(self, data: IntermType) -> T: ...


class AbstractDecoder(ABC, Generic[T, IntermType]):
    @abstractmethod
    def __call__(self, data: T) -> IntermType: ...
