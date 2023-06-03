from vampytest import reverse

from ..aliases import assert_true


def test_assert_true():
    """
    Tests whether `true` assertion succeeds.
    """
    assert_true(1)


@reverse()
def test_assert_true_reversed():
    """
    Tests whether `true` assertion fails.
    """
    assert_true(0)
