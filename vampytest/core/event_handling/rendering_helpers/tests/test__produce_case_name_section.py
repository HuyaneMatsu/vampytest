from scarletio import DEFAULT_ANSI_HIGHLIGHTER, get_highlight_streamer, iter_split_ansi_format_codes

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..result_rendering_common import produce_case_name_section


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
def test__produce_case_name_section(name, highlighter):
    """
    Tests whether ``produce_case_name_section`` works as intended.
    
    Parameters
    ----------
    name : `str`
        The test case's name.
    
    highlighter : ``None | HighlightFormatterContext``
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    highlight_streamer = get_highlight_streamer(highlighter)
    output = []
    
    for item in produce_case_name_section(name):
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
