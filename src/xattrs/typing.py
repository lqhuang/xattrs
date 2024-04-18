# SPDX-License-Identifier: BSD-3-Clause


from typing import Any, Callable, ClassVar, Protocol, TypeVar

from dataclasses import Field

from attrs import AttrsInstance


# copy from typeshed/stdlib/dataclasses.pyi
class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


XattrsInstance = TypeVar("XattrsInstance", AttrsInstance, DataclassInstance)

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

ProtocolPrimitive = TypeVar("ProtocolPrimitive")
IntermType = TypeVar("IntermType")  # interchange format / intermediary / bridge

ConstructHook = Callable[[IntermType], Any]
DeconstructHook = Callable[[Any], IntermType]
