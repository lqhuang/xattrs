# SPDX-License-Identifier: BSD-3-Clause


class XAttrsException(Exception):
    """
    Base class for all exceptions raised by ``xattrs``.
    """


class DispatchError(XAttrsException):
    """
    Raised when error occurs during excution of dispatching.
    """


class SingleDispatchError(DispatchError):
    """
    Raised when get a hook or apply a hook through single dispatch branch.
    """


class HookNotFoundError(DispatchError):
    """
    Raised when a hook for a type is not found from dispatch register.
    """
