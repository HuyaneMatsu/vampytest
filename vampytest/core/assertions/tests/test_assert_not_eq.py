from vampytest import reverse

from ..aliases import assert_not_eq


def test_assert_not_eq():
    """
    Tests whether `!=` assertion succeeds.
    """
    assert_not_eq(1, 2)


@reverse()
def test_assert_not_eq_reversed():
    """
    Tests whether `!=` assertion fails.
    """
    assert_not_eq(1, 1)
