# SPDX-License-Identifier: MIT
# ruff: noqa: F822
# pyright: reportUnsupportedDunderAll=false
from __future__ import annotations

from functools import partial

import attrs
import optree
from attrs import (
    NOTHING,
    Attribute,
    AttrsInstance,
    Converter,
    Factory,
    asdict,
    assoc,
    astuple,
    cmp_using,
    converters,
    evolve,
    exceptions,
    field,
    fields,
    fields_dict,
    filters,
    has,
    resolve_types,
    setters,
    validate,
    validators,
)
from attrs import define as _define

from xattrs.constants import NAMESPACE_STRUCT_DICT

# Keep the same with the `attrs` module. (except `make_class`)
# `make_class` is not a full replacement in `xattrs`.
__all__ = [*attrs.__all__]  # type: ignore[reportAttributeAccessIssue]  # noqa: PLE0604


def _attrs_flatten(inst):
    cls = inst.__class__
    fs = fields(cls)
    children = tuple(getattr(inst, f.name) for f in fs)
    return (children, fields_dict(cls), {f.name: "*" for f in fs})


def define(cls=None, **kwargs):
    def wrap(_cls):
        attrs_cls = _define(_cls, **kwargs)

        def _attrs_unflatten(metadata, children):
            return attrs_cls(**{f.name: v for f, v in zip(fields(attrs_cls), children)})

        optree.register_pytree_node(
            attrs_cls, _attrs_flatten, _attrs_unflatten, namespace=NAMESPACE_STRUCT_DICT
        )

        return attrs_cls

    if cls is None:
        return wrap

    return wrap(cls)


mutable = define
frozen = partial(define, frozen=True, on_setattr=None)

__getattr__ = __import__("attrs").__getattr__
