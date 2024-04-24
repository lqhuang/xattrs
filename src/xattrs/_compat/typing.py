# SPDX-License-Identifier: BSD-3-Clause
# ruff: noqa: F401, UP035
from typing import *  # type: ignore # noqa: F403
from typing import __all__

from sys import version_info

# Overwrite the original `typing` module from `typing_extensions`
# for typing compatibility

if version_info < (3, 12):
    from typing_extensions import TypeAliasType, override

if version_info < (3, 11):
    from typing_extensions import Any  # behavior changed in 3.11
    from typing_extensions import NamedTuple  # behavior changed in 3.11
    from typing_extensions import (
        NewType,  # behavior changed in 3.10, performance improved in 3.11
    )
    from typing_extensions import TypedDict  # behavior changed in 3.11
    from typing_extensions import final  # behavior changed in 3.11
    from typing_extensions import get_type_hints  # behavior changed in 3.11
    from typing_extensions import overload  # behavior changed in 3.11
    from typing_extensions import (
        LiteralString,
        Never,
        NotRequired,
        Required,
        Self,
        TypeVarTuple,
        Unpack,
        assert_never,
        assert_type,
        clear_overloads,
        dataclass_transform,
        get_overloads,
        reveal_type,
    )

if version_info < (3, 10):
    from typing_extensions import (
        Annotated,
        Callable,
        Concatenate,
        Generic,
        ParamSpec,
        ParamSpecArgs,
        ParamSpecKwargs,
        TypeAlias,
        TypeGuard,
        is_typeddict,
    )

if version_info < (3, 9, 1):
    # from docs.python.org/3/library/typing.html#typing.Literal
    # _Changed in version 3.9.1_: `Literal` now de-duplicates parameters.
    from typing_extensions import Literal
