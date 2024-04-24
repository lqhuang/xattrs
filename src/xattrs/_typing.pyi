from sys import version_info

if version_info >= (3, 11):
    from typing import TypeVarTuple, TypeVar, TypeAlias, Any, Mapping

    T = TypeVar("T")
    Ts = TypeVarTuple("Ts")

    PosArgs: TypeAlias = tuple[Any, ...]
    VarArgs: TypeAlias = tuple[*Ts]
    KwArgs: TypeAlias = tuple[*Ts, Mapping]

    ArgsTree = tuple | PosArgs | VarArgs | KwArgs
