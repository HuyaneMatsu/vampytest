from scarletio import DEFAULT_ANSI_HIGHLIGHTER

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..parameter_rendering import _render_parameter_representation_into


def _iter_options():
    yield (
        'remilia',
        12,
        None,
        'remilia = 12\n',
    )
    
    yield (
        'remilia',
        'satori',
        None,
        'remilia = \'satori\'\n',
    )
    
    yield (
        'remilia',
        int,
        None,
        'remilia = int\n',
    )
    
    # with highlighter
    yield (
        'remilia',
        int,
        DEFAULT_ANSI_HIGHLIGHTER,
        'remilia = int\n',
    )
    
    # no name
    yield (
        None,
        12,
        None,
        '12\n',
    )


@_(call_from(_iter_options()).returning_last())
def test__render_parameter_representation_into(parameter_name, parameter_value, highlighter):
    """
    Tests whether ``_render_parameter_representation_into`` works as intended.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name.
    
    parameter_value : `object`
        The parameter's value.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    into = _render_parameter_representation_into(parameter_name, parameter_value, highlighter, [])
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
