from __future__ import annotations

from typing import Any

from dataclasses import dataclass
from dataclasses import field as dataclass_field

import pytest
from attr import field as attrs_filed
from attrs import define
from attrs import field as attrs_field
from hypothesis import given
from hypothesis import strategies as st

from xattrs._metadata import _gen_field_filter, _gen_field_key_serializer, _Metadata
from xattrs._uni import _fields
from xattrs.converters import to_camel, to_const, to_kebab
from xattrs.filters import exclude_if_default, exclude_if_false, keep_include


@pytest.fixture(scope="class")
def make_field_with_filter():
    def gen(field_kwargs, init_kwargs, metadata: _Metadata):

        @define
        class A:
            x: Any = attrs_filed(**field_kwargs) | metadata

        @dataclass
        class D:
            x: Any = dataclass_field(**field_kwargs) | metadata

        return A(**init_kwargs), D(**init_kwargs)

    return gen


@pytest.fixture(scope="class")
def make_field_with_alias():
    def gen(field_kwargs, init_kwargs, metadata: _Metadata):

        @define
        class A:
            snake_name: Any = attrs_filed(**field_kwargs) | metadata

        @dataclass
        class D:
            snake_name: Any = dataclass_field(**field_kwargs) | metadata

        return A(**init_kwargs), D(**init_kwargs)

    return gen


class TestMetadata:
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
    def test_metadata__ror_with_attribute(
        self, deco_func, field_func, field_kwargs, meta_kwargs
    ):
        created_field = field_func(**field_kwargs)
        new_field = created_field | _Metadata(**meta_kwargs)
        assert type(new_field) == type(created_field)
        for k, v in meta_kwargs.items():
            assert new_field.metadata.get(k) == v

        @deco_func
        class C:
            x: int = field_func(**field_kwargs) | _Metadata(**meta_kwargs)

        for f in _fields(C):  # pyright: ignore[reportCallIssue,reportArgumentType]
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
    def test_metadata__conflict_conf(self, meta_kwargs):
        error_msg = "Only one of 'exclude', 'exclude_if', 'exclude_if_default', 'exclude_if_false' values can be set."
        with pytest.raises(ValueError, match=error_msg):
            _Metadata(**meta_kwargs)


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
            ({"exclude_if_false": True}, lambda f, v: True, exclude_if_false),
            ({"exclude_if_false": True}, lambda f, v: False, exclude_if_false),
            ({"exclude_if_false": False}, lambda f, v: True, keep_include),
            ({"exclude_if_false": False}, lambda f, v: False, keep_include),
            ({"exclude_if_false": False}, None, keep_include),
            ({}, None, keep_include),
            ({}, lambda f, v: v // 2 == 0, lambda f, v: v // 2 == 0),
        ],
    )
    def test_gen_field_filter__default(
        self,
        make_field_with_filter,
        field_kwargs,
        init_kwargs,
        filter_conf,
        scope_filter,
        expected_filter_func,
    ):
        attrs_inst, dataclass_inst = make_field_with_filter(
            field_kwargs, init_kwargs, _Metadata(**filter_conf)
        )
        for f in _fields(attrs_inst):
            _filter = _gen_field_filter(f, scope_filter)
            val = getattr(attrs_inst, f.name)
            assert _filter(f, val) == expected_filter_func(f, val)
            break

        for f in _fields(dataclass_inst):
            _filter = _gen_field_filter(f, scope_filter)
            val = getattr(dataclass_inst, f.name)
            assert _filter(f, val) == expected_filter_func(f, val)
            break


class TestGenFieldKeySerializer:

    @pytest.mark.parametrize(
        ("alias_conf", "scope_alias", "expected_alias_func"),
        [
            ({"alias": "x"}, None, lambda s: "x"),
            ({"alias": "x"}, lambda s: "aaa", lambda s: "x"),
            ({"alias_converter": "kebab-case"}, lambda s: False, to_kebab),
            ({"alias_converter": "camelCase"}, None, to_camel),
            ({"alias_converter": lambda s: s.upper()}, lambda s: "xx", to_const),
            ({}, lambda s: "xxx", lambda s: "xxx"),
            ({}, None, lambda s: s),
            ({}, to_const, lambda s: s.upper()),
        ],
    )
    def test_gen_field_filter__default(
        self,
        make_field_with_alias,
        alias_conf,
        scope_alias,
        expected_alias_func,
    ):
        attrs_inst, dataclass_inst = make_field_with_alias(
            {}, {"snake_name": None}, _Metadata(**alias_conf)
        )
        for f in _fields(attrs_inst):
            _filter = _gen_field_key_serializer(f, scope_alias)
            assert _filter(f.name) == expected_alias_func(f.name)
        for f in _fields(dataclass_inst):
            _filter = _gen_field_key_serializer(f, scope_alias)
            assert _filter(f.name) == expected_alias_func(f.name)
