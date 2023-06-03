from vampytest import reverse

from ..aliases import assert_eq


def test_assert_eq():
    """
    Tests whether `eq` assertion succeeds.
    """
    assert_eq(1, 1)


@reverse()
def test_assert_eq_reversed():
    """
    Tests whether `eq` assertion fails.
    """
    assert_eq(1, 2)


@reverse()
async def test_assert_eq_async_reversed():
    """
    Tests whether `eq` assertion fails in an async test.
    """
    assert_eq(1, 2)
