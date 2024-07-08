from __future__ import annotations

from dataclasses import is_dataclass

import pytest

from xattrs._uni import _is_dataclass_class


# TODO: add test cases
def _test__is_dataclass_with_offcial_implmentation(data):
    cls = data if isinstance(data, type) else type(data)
    assert _is_dataclass_class(cls) == is_dataclass(data)
