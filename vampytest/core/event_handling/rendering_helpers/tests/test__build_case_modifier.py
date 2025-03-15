from ....assertions import assert_instance
from ....handling import CallState
from ....utils import _
from ....wrappers import call_from

from ..case_modifiers import build_case_modifier


def _iter_options():
    yield (
        None,
        '',
    )
    
    yield (
        CallState().with_parameters(None, {'a': 'b'}),
        '[a = \'b\']',
    )
    
    yield (
        CallState().with_parameters(['a'], None),
        '[\'a\']',
    )
    
    yield (
        CallState().with_parameters(['a', 'b'], {'a': 'b', 'c': 'd'}),
        '[\'a\', \'b\', a = \'b\', c = \'d\']'
    )
    
    yield (
        CallState().with_name('orin'),
        '<orin>',
    )
    
    yield (
        CallState().with_parameters(['a'], None).with_name('orin'),
        '<orin>',
    )


@_(call_from(_iter_options()).returning_last())
def test__build_case_modifier(call_state):
    """
    Tests whether ``build_case_modifier`` works as intended.
    
    Parameters
    ----------
    positional_parameters : `None | list<object>`
        Positional parameters to the the test function with.
    
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters to the call the test function with.
    
    Returns
    -------
    output : `str`
    """
    output = build_case_modifier(call_state)
    assert_instance(output, str)
    return output
