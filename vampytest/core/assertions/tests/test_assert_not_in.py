from vampytest import reverse

from ..aliases import assert_not_in


def test_assert_not_in():
    """
    Tests whether `not-in` assertion succeeds.
    """
    assert_not_in(1, [])


@reverse()
def test_assert_not_in_reversed():
    """
    Tests whether `not-in` assertion fails.
    """
    assert_not_in(1, [1])
