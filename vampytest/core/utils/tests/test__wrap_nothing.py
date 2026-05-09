from vampytest import assert_is

from ..wrap_nothing import _


def test__wrap_nothing():
    """
    Tests whether `_` works as intended.
    """
    a = object()
    assert_is(a, _(a))
