from __future__ import annotations

from typing import Any

from collections import OrderedDict
from dataclasses import dataclass

import pytest
from attrs import frozen
from hypothesis import given
from hypothesis import strategies as st

from xattrs._astree import astree

MAPPING_TYPES = (dict, OrderedDict)
SEQUENCE_TYPES = (list, tuple)


@pytest.fixture(scope="session")
def A():
    """
    Return an attrs class
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


class TestAsTuple:
    """
    Tests for `astree`.
    """

    @given(seq=st.sampled_from(SEQUENCE_TYPES))
    def test_attrs(self, A, seq):
        acutal = astree(A(A(1, 2), A(3, 4)), tuple_factory=seq)
        expected = seq((seq((1, 2)), seq((3, 4))))
        assert acutal == expected

    @given(seq=st.sampled_from(SEQUENCE_TYPES))
    def test_dataclasses(self, D, seq):
        acutal = astree(D(D("1", 2), D(3, "4")), tuple_factory=seq)
        expected = seq((seq(("1", 2)), seq((3, "4"))))
        assert acutal == expected

    def test_mixed_attrs_dataclass(self, A, D):
        actual = (("1", "2"), (3, 4))
        expected = astree(A(A("1", "2"), D(3, 4)))
        assert actual == expected

        actual = (("1", 2), (3, "4"))
        expected = astree(D(A("1", 2), D(3, "4")))
        assert actual == expected

    def test_mapping(
        self,
        A,
        D,
    ):
        """
        contains mapping
        """
        actual = astree(D(1, {"x": 2, "y": 3}))
        expected = (1, (("x", 2), ("y", 3)))
        assert actual == expected

        actual = astree(
            A(
                1,
                (A(2, 3), D(4, 5), {"x": "6", "y": "7"}),
            )
        )
        expected = (
            1,
            ((2, 3), (4, 5), (("x", "6"), ("y", "7"))),
        )
        assert actual == expected
