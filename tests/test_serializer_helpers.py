from __future__ import annotations

from typing import Any, Callable

from dataclasses import dataclass
from dataclasses import field as dataclass_field

import pytest
from attr import field as attrs_filed
from attrs import define
from hypothesis import given
from hypothesis import strategies as st

from xattrs._metadata import _gen_field_filter, _gen_field_key_serializer, _Metadata
from xattrs._serde import _gen_serializer_helpers
from xattrs._uni import _fields
from xattrs.filters import exclude_if_default, exclude_if_false, keep_include


@pytest.fixture(scope="class")
def make_configed_serde():

    def gen(deco_func, field_func, serde: Callable):
        @deco_func
        class C:
            x: int = field_func()
            y: int = 100

        return C

    return gen


@pytest.fixture(scope="class")
def make_configed_field():
    def gen(field_kwargs, init_kwargs, metadata: _Metadata):

        @define
        class A:
            x: Any = attrs_filed(**field_kwargs) | metadata

        @dataclass
        class D:
            x: Any = dataclass_field(**field_kwargs) | metadata

        return A(**init_kwargs), D(**init_kwargs)

    return gen


class TestGenFieldFilter:

    @pytest.mark.parametrize(
        ("field_kwargs", "init_kwargs"),
        [
            ({"default": 100}, {"x": 100}),
            ({"default": None}, {"x": 100}),
            ({"default": None}, {"x": 200}),
            ({}, {"x": 0}),
            ({"default": 1000}, {"x": 0}),
            ({"default": 355}, {"x": 355}),
            ({"default": 123}, {"x": 200}),
            ({"default": 123}, {"x": 123}),
        ],
    )
    @pytest.mark.parametrize(
        ("filter_conf", "scope_filter", "expected_filter_func"),
        [
            ({"exclude": True}, None, lambda f, v: False),
            ({"exclude": False}, lambda f, v: True, lambda f, v: True),
            ({"exclude": False}, lambda f, v: False, lambda f, v: True),
            (
                {"exclude_if": lambda f, v: v // 2 == 0},
                lambda f, v: False,
                lambda f, v: v // 2 == 0,
            ),
            (
                {"exclude_if": lambda f, v: v // 2 != 0},
                None,
                lambda f, v: v // 2 != 0,
            ),
            ({"exclude_if_default": True}, lambda f, v: True, exclude_if_default),
            (
                {"exclude_if_default": True},
                lambda f, v: False,
                exclude_if_default,
            ),
            (
                {"exclude_if_default": False},
                lambda f, v: False,
                keep_include,
            ),
            ({"exclude_if_default": False}, None, keep_include),
            ({"exclude_if_false": True}, lambda f, v: True, lambda f, v: bool(v)),
            ({"exclude_if_false": True}, lambda f, v: False, lambda f, v: bool(v)),
            ({"exclude_if_false": False}, lambda f, v: True, keep_include),
            ({"exclude_if_false": False}, lambda f, v: False, keep_include),
            ({"exclude_if_false": False}, None, keep_include),
            ({}, None, keep_include),
            ({}, lambda f, v: v // 2 == 0, lambda f, v: v // 2 == 0),
        ],
    )
    def test_gen_field_filter__default(
        self,
        make_configed_field,
        field_kwargs,
        init_kwargs,
        filter_conf,
        scope_filter,
        expected_filter_func,
    ):
        attrs_inst, dataclass_inst = make_configed_field(
            field_kwargs, init_kwargs, _Metadata(**filter_conf)
        )
        for f in _fields(attrs_inst):
            _filter = _gen_field_filter(f, scope_filter)
            val = getattr(attrs_inst, f.name)
            assert _filter(f, val) == expected_filter_func(f, val)

        for f in _fields(dataclass_inst):
            _filter = _gen_field_filter(f, scope_filter)
            val = getattr(dataclass_inst, f.name)
            assert _filter(f, val) == expected_filter_func(f, val)


class TestGenFieldKeySerializer:
    ...

    # @pytest.mark.parametrize(
    #     ("deco_func", "field_func"),
    #     [
    #         (define, attrs_filed),
    #         (dataclass, dataclass_field),
    #     ],
    # )
    # @pytest.mark.parametrize(
    #     ("filter_conf", "filter_func"),
    #     [
    #         ({"exclude": True}, {}),
    #         ({"exclude": False}, {}),
    #         ({"exclude": True}, lambda x: False),
    #         ({"exclude": False}, lambda x: True),
    #     ],
    # )
    # @pytest.mark.parametrize("scope_filter", [None, lambda x: True])
    # def test_gen_field_filter__default(
    #     self, make_configed_field, deco_func, field_func, filter_func, scope_filter
    # ):
    #     attribute = make_configed_field(define, deco_func, field_func)

    #     assert _gen_field_filter(attribute, filter_func) == attribute


class TestGenSerializerHelpers: ...
