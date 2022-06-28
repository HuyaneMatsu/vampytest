from .. import assert_id

from vampytest import revert


def test_assert_id():
    """
    Tests whether `is` assertion succeeds.
    """
    a = object()
    
    assert_id(a, a)


@revert()
def test_assert_id_reverted():
    """
    Tests whether `is` assertion fails.
    """
    a = object()
    b = object()
    
    assert_id(a, b)
