from vampytest import revert

from ..aliases import assert_true


def test_assert_true():
    """
    Tests whether `true` assertion succeeds.
    """
    assert_true(1)


@revert()
def test_assert_true_reverted():
    """
    Tests whether `true` assertion fails.
    """
    assert_true(0)
