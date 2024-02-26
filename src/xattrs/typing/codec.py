from __future__ import annotations

from typing import Generic, TypeVar

from abc import ABC, abstractmethod

# Traits


A = TypeVar("A")

IF = TypeVar("IF")  # interchange format
PYOBJ = TypeVar("PYOBJ")  # python object


class AbstrctCodec(ABC, Generic[A, PYOBJ]):
    decoder: AbstrctDecoder[PYOBJ, A]
    encoder: AbstrctEncoder[A, PYOBJ]


class AbstrctDecoder(ABC, Generic[PYOBJ, A]):
    @abstractmethod
    def __call__(self, data: PYOBJ) -> A: ...


class AbstrctEncoder(ABC, Generic[A, PYOBJ]):
    @abstractmethod
    def __call__(self, data: A) -> PYOBJ: ...


class AbstrctParser(ABC, Generic[IF]):
    @abstractmethod
    def __call__(self, data: str | bytes) -> IF: ...
