from .. import assert_false

from vampytest import revert


def test_assert_false():
    """
    Tests whether `false` assertion succeeds.
    """
    assert_false(0)


@revert()
def test_assert_false_reverted():
    """
    Tests whether `false` assertion fails.
    """
    assert_false(1)
