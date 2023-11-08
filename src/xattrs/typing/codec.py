from __future__ import annotations

from typing import Any, Generic, TypeVar

from abc import ABC, abstractmethod

# Traits


A = TypeVar("A")

IF = TypeVar("IF")  # interchange format


class AbstrctCodec(ABC, Generic[A, IF]):
    decoder: AbstrctDecoder[IF, A]
    encoder: AbstrctEncoder[A, IF]


class AbstrctDecoder(ABC, Generic[IF, A]):
    @abstractmethod
    def __call__(self, data: IF) -> A:
        ...


class AbstrctEncoder(ABC, Generic[A, IF]):
    @abstractmethod
    def __call__(self, data: A) -> IF:
        ...


class AbstrctParser(ABC, Generic[IF]):
    def parse(self, data: str | bytes) -> A:
        return self(data)

    @abstractmethod
    def __call__(self, data: bytes) -> Any:
        ...
