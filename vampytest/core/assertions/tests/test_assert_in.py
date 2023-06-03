from vampytest import reverse

from ..aliases import assert_in


def test_assert_in():
    """
    Tests whether `in` assertion succeeds.
    """
    assert_in(1, [1])


@reverse()
def test_assert_in_reversed():
    """
    Tests whether `in` assertion fails.
    """
    assert_in(1, [])
