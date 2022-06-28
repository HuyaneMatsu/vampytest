from .. import assert_not_in

from vampytest import revert


def test_assert_not_in():
    """
    Tests whether `not-in` assertion succeeds.
    """
    assert_not_in(1, [])


@revert()
def test_assert_not_in_reverted():
    """
    Tests whether `not-in` assertion fails.
    """
    assert_not_in(1, [1])
