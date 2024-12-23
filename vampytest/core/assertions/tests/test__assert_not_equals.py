from ...utils import _
from ...wrappers import call_from

from ..exception import AssertionException
from ..top_level import assert_not_equals


def _iter_options():
    yield 0, 1, {}, False
    yield 0, 0, {}, True
    yield 0, 1, {'reverse': True}, True
    yield 0, 0, {'reverse': True}, False


@_(call_from(_iter_options()).returning_last())
def test__assert_not_equals(value_0, value_1, keyword_parameters):
    """
    Tests whether ``assert_not_equals`` works as intended.
    
    Parameters
    ----------
    value_0 : `object`
        The first value to assert with.
    
    value_1 : `object`
        The second value to assert with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass to the assertion.
    
    Returns
    -------
    failed : `bool`
    """
    try:
        assert_not_equals(value_0, value_1, **keyword_parameters)
    except AssertionException:
        failed = True
    else:
        failed = False
    
    return failed
