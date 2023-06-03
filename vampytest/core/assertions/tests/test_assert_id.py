from vampytest import reverse

from ..aliases import assert_id


def test_assert_id():
    """
    Tests whether `is` assertion succeeds.
    """
    a = object()
    
    assert_id(a, a)


@reverse()
def test_assert_id_reversed():
    """
    Tests whether `is` assertion fails.
    """
    a = object()
    b = object()
    
    assert_id(a, b)
