from .. import assert_eq

from vampytest import revert


def test_assert_eq():
    """
    Tests whether `eq` assertion succeeds.
    """
    assert_eq(1, 2)


@revert()
def test_assert_eq_reverted():
    """
    Tests whether `eq` assertion fails.
    """
    assert_eq(1, 2)
