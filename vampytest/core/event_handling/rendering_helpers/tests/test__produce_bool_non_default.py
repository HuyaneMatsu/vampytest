from scarletio import DEFAULT_ANSI_HIGHLIGHTER, get_highlight_streamer, iter_split_ansi_format_codes

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..parameter_rendering import _produce_bool_non_default


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
def test__produce_bool_non_default(parameter_name, parameter_value, default, highlighter):
    """
    Tests whether ``_produce_bool_non_default`` works as intended.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name.
    
    parameter_value : `bool`
        The parameter's value.
    
    default : `bool`
        Default value.
    
    highlighter : ``None | HighlightFormatterContext``
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    highlight_streamer = get_highlight_streamer(highlighter)
    output = []
    for item in _produce_bool_non_default(parameter_name, parameter_value, default):
        output.extend(highlight_streamer.asend(item))
        
    output.extend(highlight_streamer.asend(None))
    
    for element in output:
        assert_instance(element, str)
    
    output_string = ''.join(output)
    split = [*iter_split_ansi_format_codes(output_string)]
    assert_eq(
        any(item[0] for item in split),
        (highlighter is not None),
    )
    
    return ''.join([item[1] for item in split if not item[0]])
