from ...utils import _
from ...wrappers import call_from

from ..exception import AssertionException
from ..top_level import assert_subtype


def _iter_options():
    yield int, (int, ), {}, False
    yield str, (int, ), {}, True
    yield int, (int, ), {'reverse': True}, True
    yield str, (int, ), {'reverse': True}, False
    
    # sub-type
    yield bool, (int, ), {}, False
    yield int, (bool, ), {}, True
    
    # accepted_types
    yield int, (int, float), {}, False
    yield str, (int, float), {}, True
    yield int, (int, float), {'reverse': True}, True
    yield str, (int, float), {'reverse': True}, False
    
    # not type
    yield 1, (int, ), {}, True
    yield 1, (int, ), {'reverse': True}, False
    
    # nullable
    yield None, (int, ), {}, True
    yield None, (int, ), {'nullable': True}, False


@_(call_from(_iter_options()).returning_last())
def test__assert_subtype(value, accepted_types, keyword_parameters):
    """
    Tests whether ``assert_subtype`` works as intended.
    
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
        assert_subtype(value, *accepted_types, **keyword_parameters)
    except AssertionException:
        failed = True
    else:
        failed = False
    
    return failed
