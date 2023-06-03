from vampytest import revert

from ..aliases import assert_in


def test_assert_in():
    """
    Tests whether `in` assertion succeeds.
    """
    assert_in(1, [1])


@revert()
def test_assert_in_reverted():
    """
    Tests whether `in` assertion fails.
    """
    assert_in(1, [])
