# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import types
from typing import Literal

# Copied from CPYTHON/Lib/dataclasses.py (near line 225)
#
# Atomic immutable types which don't require any recursive handling and for which deepcopy
# returns the same object. We can provide a fast-path for these types in asdict and astuple.
_ATOMIC_TYPES = frozenset(
    {
        # Common JSON Serializable types
        types.NoneType,
        bool,
        int,
        float,
        str,
        # Other common types
        complex,
        bytes,
        # Other types that are also unaffected by deepcopy
        types.EllipsisType,
        types.NotImplementedType,
        types.CodeType,
        types.BuiltinFunctionType,
        types.FunctionType,
        type,
        range,
        property,
    }
)

SerdeStrategy = Literal["dict", "tuple", "tree", "auto_detect"]

CaseConvention = Literal[
    "lowercase",
    "UPPERCASE",
    "upper",
    "uppercase",
    "Capitalize",
    "capitalize",
    # easy to remember?
    "PascalCase",
    "camelCase",
    "snake_case",
    "CONST_CASE",
    "Ada_Case",
    "kebab-case",
    "COBOL-CASE",
    "Train-Case",
]
