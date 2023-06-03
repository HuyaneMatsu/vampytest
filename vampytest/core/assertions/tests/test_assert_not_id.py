from vampytest import reverse

from ..aliases import assert_not_id


def test_assert_not_id():
    """
    Tests whether `is-not` assertion succeeds.
    """
    a = object()
    b = object()
    
    assert_not_id(a, b)


@reverse()
def test_assert_not_id_reversed():
    """
    Tests whether `is-not` assertion fails.
    """
    a = object()
    
    assert_not_id(a, a)
