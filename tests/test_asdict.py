from __future__ import annotations

from typing import Any

from collections import OrderedDict
from dataclasses import dataclass

import pytest
from attrs import frozen
from hypothesis import given
from hypothesis import strategies as st

from xattrs._asdict import asdict

MAPPING_TYPES = (dict, OrderedDict)
SEQUENCE_TYPES = (list, tuple)


@pytest.fixture(scope="session")
def A():
    """
    Return a attrs class
    """

    @frozen
    class A:
        x: Any
        y: Any

    return A


@pytest.fixture(scope="session")
def D():
    """
    Return a dataclass class
    """

    @dataclass
    class D:
        x: Any
        y: Any

    return D


class TestAsDict:
    """
    Tests for `asdict`.
    """

    @given(dict_factory=st.sampled_from(MAPPING_TYPES))
    def test_attrs(self, A, dict_factory):
        acutal = asdict(A(A(1, 2), A(3, 4)), dict_factory=dict_factory)
        expected = {"x": {"x": 1, "y": 2}, "y": {"x": 3, "y": 4}}
        assert acutal == expected

    @given(dict_factory=st.sampled_from(MAPPING_TYPES))
    def test_dataclass(self, D, dict_factory):
        actual = {"x": {"x": "1", "y": "2"}, "y": {"x": 3, "y": 4}}
        expected = asdict(D(D("1", "2"), D(3, 4)), dict_factory=dict_factory)
        assert actual == expected

    @given(dict_factory=st.sampled_from(MAPPING_TYPES))
    def test_mixed_attrs_dataclass(self, A, D, dict_factory):
        actual = {"x": {"x": "1", "y": "2"}, "y": {"x": 3, "y": 4}}
        expected = asdict(A(A("1", "2"), D(3, 4)), dict_factory=dict_factory)
        assert actual == expected

        actual = {"x": {"x": "1", "y": "2"}, "y": {"x": 3, "y": 4}}
        expected = asdict(D(A("1", "2"), D(3, 4)), dict_factory=dict_factory)
        assert actual == expected

    @given(seq=st.sampled_from(SEQUENCE_TYPES))
    def test_lists_tuples(self, A, D, seq):
        """
        list / tuple.
        """
        actual = asdict(D(1, seq([A(2, 3), D(4, 5), "a"])))
        expected = {
            "x": 1,
            "y": seq(({"x": 2, "y": 3}, {"x": 4, "y": 5}, "a")),
        }
        assert actual == expected

        actual = asdict(A(1, seq((A(2, 3), D(4, 5), D("6", "7")))))
        expected = {
            "x": 1,
            "y": seq([{"x": 2, "y": 3}, {"x": 4, "y": 5}, {"x": "6", "y": "7"}]),
        }
