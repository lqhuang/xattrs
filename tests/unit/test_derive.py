from xattrs._compat.typing import Callable, TypeAlias

import pytest

from xattrs import derive

_StrGen: TypeAlias = Callable[..., str]


def trait1(wrapped: _StrGen) -> _StrGen:
    """add postfix "1" to wrapped return"""

    def wrapper(**kwargs):
        return wrapped(**kwargs) + "1"

    return wrapper


def trait2(wrapped: _StrGen) -> _StrGen:
    """add prefix "2" to wrapped return"""

    def wrapper(**kwargs):
        return "2" + wrapped(**kwargs)

    return wrapper


def trait3(wrapped: _StrGen) -> _StrGen:
    """reverse the return of wrapped."""

    def wrapper(**kwargs):
        return wrapped(**kwargs)[::-1]

    return wrapper


@pytest.mark.parametrize(
    ("traits", "expected_decorator"),
    [
        ([trait1], trait1),
        (
            [trait1, trait2, trait3],
            lambda x: trait3(trait2(trait1(x))),
        ),
        (
            [trait3, trait2, trait1],
            lambda x: trait1(trait2(trait3(x))),
        ),
    ],
)
def test_derive__sequence(traits, expected_decorator):

    def wrapped():
        return "hello, world"

    assert derive(*traits)(wrapped)() == expected_decorator(wrapped)()


def test_drive__empty():
    """
    Test derive() with no traits. should return identicial function as wrapped.
    """

    def wrapped(x=None):
        return x

    assert id(derive()(wrapped)) == id(wrapped)
    assert derive()(wrapped)() is None
    assert derive()(wrapped)(111111) == 111111
