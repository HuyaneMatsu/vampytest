from scarletio import DEFAULT_ANSI_HIGHLIGHTER, get_highlight_streamer, iter_split_ansi_format_codes

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..result_rendering_common import render_case_name_section_into


def _iter_options():
    # Default
    yield (
        'koishi',
        None,
        (
            '\n'
            'Named: koishi\n'
        ),
    )
    
    # Highlighted
    yield (
        'koishi',
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            '\n'
            'Named: koishi\n'
        ),
    )


@_(call_from(_iter_options()).returning_last())
def test__render_case_name_section_into(name, highlighter):
    """
    Tests whether ``render_case_name_section_into`` works as intended.
    
    Parameters
    ----------
    name : `str`
        The test case's name.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    highlight_streamer = get_highlight_streamer(highlighter)
    into = render_case_name_section_into(name, highlight_streamer, [])
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
