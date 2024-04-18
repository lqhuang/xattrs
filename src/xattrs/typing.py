# SPDX-License-Identifier: BSD-3-Clause


from typing import Any, ClassVar, Protocol, TypeVar

from dataclasses import Field

from attrs import AttrsInstance

__all__ = ["XattrsInstance"]


# copy from typeshed/stdlib/dataclasses.pyi
class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


XattrsInstance = TypeVar("XattrsInstance", AttrsInstance, DataclassInstance)

# Type Union for primitive types in Python
# https://docs.python.org/3/library/stdtypes.html
Primitives = TypeVar("Primitives", str, int, float, bool, None)
