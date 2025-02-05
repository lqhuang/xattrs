# SPDX-License-Identifier: MIT
from __future__ import annotations

from functools import partial

from optree import register_pytree_node, tree_flatten, tree_unflatten

__all__ = ["flatten", "register_de_node", "register_ser_node", "unflatten"]

_SER_NAMESPACE = "__attrs_ser__"
_DE_NAMESPACE = "__attrs_deser__"

_FLATTEN_ATTR = "__attrs_flatten__"
_UNFLATTEN_ATTR = "__attrs_unflatten__"

register_ser_node = partial(register_pytree_node, namespace=_SER_NAMESPACE)
register_de_node = partial(register_pytree_node, namespace=_DE_NAMESPACE)

# flatten = partial(tree_flatten, namespace=_TREE_NAMESPACE)
# unflatten = tree_unflatten
