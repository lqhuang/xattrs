# SPDX-License-Identifier: MIT
# ruff: noqa: F401, UP035
# mypy: disable-error-code="assignment"
from typing import *  # noqa: F403 # pyright: ignore[reportWildcardImportFromLibrary]
from typing_extensions import __all__

from sys import version_info

# Overwrite the original `typing` module from `typing_extensions`
# for typing compatibility

if version_info < (3, 12):
    from typing_extensions import TypeAliasType as TypeAliasType
    from typing_extensions import override as override

if version_info < (3, 11):
    from typing_extensions import Any as Any  # behavior changed in 3.11
    from typing_extensions import LiteralString as LiteralString
    from typing_extensions import NamedTuple as NamedTuple  # behavior changed in 3.11
    from typing_extensions import Never as Never
    from typing_extensions import (
        NewType as NewType,  # behavior changed in 3.10, performance improved in 3.11
    )
    from typing_extensions import NotRequired as NotRequired
    from typing_extensions import Required as Required
    from typing_extensions import Self as Self
    from typing_extensions import TypedDict as TypedDict  # behavior changed in 3.11
    from typing_extensions import TypeVarTuple as TypeVarTuple
    from typing_extensions import Unpack as Unpack
    from typing_extensions import assert_never as assert_never
    from typing_extensions import assert_type as assert_type
    from typing_extensions import clear_overloads as clear_overloads
    from typing_extensions import dataclass_transform as dataclass_transform
    from typing_extensions import final as final  # behavior changed in 3.11
    from typing_extensions import get_overloads as get_overloads
    from typing_extensions import (
        get_type_hints as get_type_hints,  # behavior changed in 3.11
    )
    from typing_extensions import overload as overload  # behavior changed in 3.11
    from typing_extensions import reveal_type as reveal_type

if version_info < (3, 10):
    from typing_extensions import Annotated as Annotated
    from typing_extensions import Callable as Callable
    from typing_extensions import Concatenate as Concatenate
    from typing_extensions import Generic as Generic
    from typing_extensions import ParamSpec as ParamSpec
    from typing_extensions import ParamSpecArgs as ParamSpecArgs
    from typing_extensions import ParamSpecKwargs as ParamSpecKwargs
    from typing_extensions import TypeAlias as TypeAlias
    from typing_extensions import TypeGuard as TypeGuard
    from typing_extensions import is_typeddict as is_typeddict

if version_info < (3, 9, 1):
    # from docs.python.org/3/library/typing.html#typing.Literal
    # _Changed in version 3.9.1_: `Literal` now de-duplicates parameters.
    from typing_extensions import Literal as Literal
