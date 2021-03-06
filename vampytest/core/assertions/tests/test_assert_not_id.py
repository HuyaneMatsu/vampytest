from .. import assert_not_id

from vampytest import revert


def test_assert_not_id():
    """
    Tests whether `is-not` assertion succeeds.
    """
    a = object()
    b = object()
    
    assert_not_id(a, b)


@revert()
def test_assert_not_id_reverted():
    """
    Tests whether `is-not` assertion fails.
    """
    a = object()
    
    assert_not_id(a, a)
