from vampytest import revert

from ..aliases import assert_eq


def test_assert_eq():
    """
    Tests whether `eq` assertion succeeds.
    """
    assert_eq(1, 1)


@revert()
def test_assert_eq_reverted():
    """
    Tests whether `eq` assertion fails.
    """
    assert_eq(1, 2)


@revert()
async def test_assert_eq_async_reverted():
    """
    Tests whether `eq` assertion fails in an async test.
    """
    assert_eq(1, 2)
