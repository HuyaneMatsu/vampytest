from scarletio import DEFAULT_ANSI_HIGHLIGHTER, get_highlight_streamer, iter_split_ansi_format_codes

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
    highlight_streamer = get_highlight_streamer(highlighter)
    into = _render_parameter_representation_into(parameter_name, parameter_value, highlight_streamer, [])
    into.extend(highlight_streamer.asend(None))
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    output_string = ''.join(into)
    split = [*iter_split_ansi_format_codes(output_string)]
    assert_eq(
        any(item[0] for item in split),
        (highlighter is not None),
    )
    
    return ''.join([item[1] for item in split if not item[0]])
