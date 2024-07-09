from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field as dataclass_field

import pytest
from attrs import define
from attrs import field as attrs_field

from xattrs._metadata import _Metadata
from xattrs._uni import _fields


@pytest.mark.parametrize(
    ("deco_func", "field_func"),
    [(define, attrs_field), (dataclass, dataclass_field)],
)
@pytest.mark.parametrize(
    "field_kwargs",
    [
        {"default": 3},
        {"metadata": {"exclude": False}},
        {"init": False, "metadata": {"alias": "whatever", "exclude": True}},
    ],
)
@pytest.mark.parametrize(
    "meta_kwargs",
    [
        {"alias": "int_field"},
        {"exclude": True},
        {"converter_to": str},
        {"alias": "int_field", "exclude": True, "converter_to": str},
    ],
)
def test_metadata__ror_with_attribute(deco_func, field_func, field_kwargs, meta_kwargs):
    created_field = field_func(**field_kwargs)
    new_field = created_field | _Metadata(**meta_kwargs)
    assert type(new_field) == type(created_field)
    for k, v in meta_kwargs.items():
        assert new_field.metadata.get(k) == v

    @deco_func
    class A:
        x: int = field_func(**field_kwargs) | _Metadata(**meta_kwargs)

    for f in _fields(A):
        for k, v in meta_kwargs.items():
            assert f.metadata.get(k) == v


@pytest.mark.parametrize(
    "meta_kwargs",
    [
        {"exclude": True, "exclude_if": lambda x: x == 3},
        {"exclude": False, "exclude_if_default": True},
        {"exclude": False, "exclude_if_false": True},
        {"exclude": True, "exclude_if_default": False},
        {"exclude_if": lambda x: x == 3, "exclude_if_false": False},
    ],
)
def test_metadata__conflict_conf(meta_kwargs):
    error_msg = "Only one of 'exclude', 'exclude_if', 'exclude_if_default', 'exclude_if_false' values can be set."
    with pytest.raises(ValueError, match=error_msg):
        _Metadata(**meta_kwargs)
