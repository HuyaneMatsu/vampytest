from ...utils import _
from ...wrappers import call_from

from ..exception import AssertionException
from ..top_level import assert_instance


def _iter_options():
    yield 0, (str, ), {}, True
    yield 1, (int, ), {}, False
    yield 0, (str, ), {'reverse': True}, False
    yield 1, (int, ), {'reverse': True}, True
    
    # accepted_types
    yield 0, (str, float, ), {}, True
    yield 1, (int, float, ), {}, False
    yield 0, (str, float, ), {'reverse': True}, False
    yield 1, (int, float, ), {'reverse': True}, True
    
    # accept_subtypes
    yield True, (int, ), {}, False
    yield True, (int, ), {'accept_subtypes': False}, True
    
    # nullable
    yield None, (int, ), {}, True
    yield None, (int, ), {'nullable': True}, False


@_(call_from(_iter_options()).returning_last())
def test__assert_instance(value, accepted_types, keyword_parameters):
    """
    Tests whether ``assert_instance`` works as intended.
    
    Parameters
    ----------
    value : `object`
        Object to check.
    
    accepted_types : `tuple<type, ...>`
        Accepted types.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass to the assertion.
    
    Returns
    -------
    failed : `bool`
    """
    try:
        assert_instance(value, *accepted_types, **keyword_parameters)
    except AssertionException:
        failed = True
    else:
        failed = False
    
    return failed
