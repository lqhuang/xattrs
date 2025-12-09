# SPDX-License-Identifier: MIT
from __future__ import annotations

from xattrs._typing import DataclassInstance

from dataclasses import (
    KW_ONLY,
    MISSING,
    Field,
    FrozenInstanceError,
    InitVar,
    asdict,
    astuple,
    field,
    fields,
    is_dataclass,
    replace,
)
from dataclasses import dataclass as _dataclass

import optree

from xattrs.constants import METANAME

# Keep the same with the `dataclasses` module of std lib, except `make_dataclass`.
# `make_dataclass` is not a full replacement  in `xattrs`.
__all__ = [
    "KW_ONLY",
    "MISSING",
    "Field",
    "FrozenInstanceError",
    "InitVar",
    "asdict",
    "astuple",
    "dataclass",
    "field",
    "fields",
    "is_dataclass",
    # "make_dataclass",
    "replace",
]


def _dataclass_flatten(ins: DataclassInstance):
    return (ins.__dict__, fields(ins))  # type: ignore[reportArgumentType]


def dataclass(  # noqa: PLR0913
    cls,
    /,
    *,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    match_args=True,
    kw_only=False,
    slots=False,
):
    def wrap(_cls):
        dataclass_cls = _dataclass(
            _cls,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
            match_args=match_args,
            kw_only=kw_only,
            slots=slots,
        )

        def _dataclass_unflatten(metadata, children) -> DataclassInstance:
            return dataclass_cls(**metadata)

        optree.register_pytree_node(
            dataclass_cls, _dataclass_flatten, _dataclass_unflatten, namespace=METANAME
        )

        return dataclass_cls

    if cls is None:
        return wrap

    return wrap(cls)
