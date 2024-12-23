from ....assertions import assert_instance
from ....utils import _
from ....wrappers import call_from

from ..result_modifier_parameters import render_result_modifier_parameters


def _iter_options():
    yield None, ''
    yield (None, None), ''
    yield (None, {'a': 'b'}), '[a = \'b\']'
    yield (['a'], None), '[\'a\']'
    yield (['a', 'b'], {'a': 'b', 'c': 'd'}),'[\'a\', \'b\', a = \'b\', c = \'d\']'


@_(call_from(_iter_options()).returning_last())
def test__render_result_modifier_parameters(parameters):
    """
    Tests whether ``render_result_modifier_parameters`` works as intended.
    
    Parameters
    ----------
    modifier_parameters : `None | (None | list<object>, None | dict<str, object)`
        Positional - keyword parameters pair.
    
    Returns
    -------
    output : `str`
    """
    into = render_result_modifier_parameters(parameters, [])
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    return ''.join(into)
