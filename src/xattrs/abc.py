# SPDX-License-Identifier: MIT
# mypy: disable-error-code="empty-body"
from __future__ import annotations

from types import MappingProxyType
from xattrs._compat.typing import TYPE_CHECKING, Any, Callable, Generic
from xattrs._typing import SingleDispatchCallable, T, T_co, T_contra, T_interm, T_proto

from abc import abstractmethod

if TYPE_CHECKING:
    from xattrs._typing import ConstructHook, DeconstructHook, Dispatchable


class AbstractSerializer(Generic[T_contra, T_co]):
    """
    Interface for custom class serializer.

    This protocol is intended to be used for custom class serializer.

    >>> from datetime import datetime
    >>>
    >>> class MySerializer(Serializer):
    ...     @dispatch
    ...     def serialize(self, value: datetime) -> str:
    ...         return value.strftime("%d/%m/%y")
    """

    def __call__(self, value: T_contra, *, inst=None, attr=None, **kwargs) -> T_co: ...


class AbstractDeserializer(Generic[T_contra, T]):
    """
    Interface for custom class deserializer.

    This protocol is intended to be used for custom class deserializer.

    >>> from datetime import datetime
    >>>
    >>> class MyDeserializer(Deserializer):
    ...     @dispatch
    ...     def deserialize(self, cls: type[datetime], value: Any) -> datetime:
    ...         return datetime.strptime(value, "%d/%m/%y")
    """

    def __call__(
        self, value: T_contra, cls: type[T], *, inst=None, attr=None, **kwargs
    ) -> T: ...


class AbstractSerDe(Generic[T, T_proto, T_contra]):
    serializer: AbstractSerializer[T, T_proto]
    deserializer: AbstractDeserializer[T_contra, T_co]

    def serialize(self, value: T, **kwargs) -> T_proto:
        return self.serializer(value, **kwargs)

    def deserialize(self, value: T_contra, cls: type[T_co], **kwargs) -> T_co:
        return self.deserializer(value, cls, **kwargs)


###############################################################################


class AbstractDispatcher(Generic[T]):
    _registry: MappingProxyType[str, SingleDispatchCallable[T]]

    @abstractmethod
    def dispatch(self, cls: Dispatchable[T]) -> Callable[..., T]: ...

    @abstractmethod
    def register(
        self, cls: Dispatchable[T], func: Callable[..., T]
    ) -> Callable[..., T]: ...
