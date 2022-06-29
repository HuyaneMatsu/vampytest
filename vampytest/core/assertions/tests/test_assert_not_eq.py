from .. import assert_not_eq

from vampytest import revert


def test_assert_not_eq():
    """
    Tests whether `!=` assertion succeeds.
    """
    assert_not_eq(1, 2)


@revert()
def test_assert_not_eq_reverted():
    """
    Tests whether `!=` assertion fails.
    """
    assert_not_eq(1, 1)
