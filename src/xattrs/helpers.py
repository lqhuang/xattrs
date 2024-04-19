# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

from xattrs.typing import T_hook, T_pyobj


def single_dispatch_not_found(c: type[T_pyobj]) -> T_hook:
    raise NotImplementedError(f"Hook for type {c} not found.")
