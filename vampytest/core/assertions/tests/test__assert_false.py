from ...utils import _
from ...wrappers import call_from

from ..exception import AssertionException
from ..top_level import assert_false


def _iter_options():
    yield 0, {}, False
    yield 1, {}, True
    yield 0, {'reverse': True}, True
    yield 1, {'reverse': True}, False


@_(call_from(_iter_options()).returning_last())
def test__assert_false(value, keyword_parameters):
    """
    Tests whether ``assert_false`` works as intended.
    
    Parameters
    ----------
    value : `object`
        The value to assert with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass to the assertion.
    
    Returns
    -------
    failed : `bool`
    """
    try:
        assert_false(value, **keyword_parameters)
    except AssertionException:
        failed = True
    else:
        failed = False
    
    return failed
