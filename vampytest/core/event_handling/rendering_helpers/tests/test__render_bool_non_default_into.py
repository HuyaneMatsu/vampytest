from scarletio import DEFAULT_ANSI_HIGHLIGHTER

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..parameter_rendering import _render_bool_non_default_into


def _iter_options():
    yield (
        'remilia',
        True,
        False,
        None,
        'remilia = True\n',
    )
    
    yield (
        'remilia',
        False,
        False,
        None,
        '',
    )
    
    yield (
        'remilia',
        True,
        True,
        None,
        '',
    )
    
    yield (
        'remilia',
        False,
        True,
        None,
        'remilia = False\n',
    )
    
    # with highlighter
    yield (
        'remilia',
        False,
        True,
        DEFAULT_ANSI_HIGHLIGHTER,
        'remilia = False\n',
    )
    
    # no name
    yield (
        None,
        True,
        False,
        None,
        'True\n',
    )
    
    yield (
        None,
        False,
        False,
        None,
        '',
    )


@_(call_from(_iter_options()).returning_last())
def test__render_bool_non_default_into(parameter_name, parameter_value, default, highlighter):
    """
    Tests whether ``_render_bool_non_default_into`` works as intended.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name.
    
    parameter_value : `bool`
        The parameter's value.
    
    default : `bool`
        Default value.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    into = _render_bool_non_default_into(parameter_name, parameter_value, default, highlighter, [])
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
