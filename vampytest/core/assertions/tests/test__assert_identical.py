from ...utils import _
from ...wrappers import call_from

from ..exception import AssertionException
from ..top_level import assert_identical


def _iter_options():
    yield None, 1, {}, True
    yield None, None, {}, False
    yield None, 1, {'reverse': True}, False
    yield None, None, {'reverse': True}, True


@_(call_from(_iter_options()).returning_last())
def test__assert_identical(value_0, value_1, keyword_parameters):
    """
    Tests whether ``assert_identical`` works as intended.
    
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
        assert_identical(value_0, value_1, **keyword_parameters)
    except AssertionException:
        failed = True
    else:
        failed = False
    
    return failed
