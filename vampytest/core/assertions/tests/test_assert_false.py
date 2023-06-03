from vampytest import reverse

from ..aliases import assert_false


def test_assert_false():
    """
    Tests whether `false` assertion succeeds.
    """
    assert_false(0)


@reverse()
def test_assert_false_reversed():
    """
    Tests whether `false` assertion fails.
    """
    assert_false(1)
