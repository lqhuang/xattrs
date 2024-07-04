# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import pytest
from xattrs.converters import to_camel, to_pascal, to_const, to_kebab, to_snake
from xattrs.converters import to_secret


class TestStringConverters:
    def test_to_camel(self): ...


@pytest.mark.parametrize(
    ("value", "expected", "extra"),
    [
        ("foo", "******", {}),
        ("foo------bar", "######", {"marker": "#"}),
        ("asdfasdfadfbar", "###", {"marker": "#", "length": 3}),
        ("asdfasdfadfbar", "**************", {"length": None}),
    ],
)
def test_to_secret(value, expected, extra):
    assert to_secret(value, **extra) == expected
