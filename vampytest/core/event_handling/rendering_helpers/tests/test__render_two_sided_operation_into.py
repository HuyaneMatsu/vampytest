from scarletio import HIGHLIGHT_TOKEN_TYPES, get_highlight_streamer, iter_split_ansi_format_codes

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..assertion_rendering import _render_two_sided_operation_into


def _iter_options():
    yield (
        [
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '+'),
        ],
        None,
        'operation = value_0 + value_1\n',
    )


@_(call_from(_iter_options()).returning_last())
def test__render_two_sided_operation_into(operation, highlighter):
    """
    Tests whether ``_render_two_sided_operation_into`` works as intended.
    
    Parameters
    ----------
    operation : `str`
        The operation between the two sides.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    highlight_streamer = get_highlight_streamer(highlighter)
    into = _render_two_sided_operation_into(operation, highlight_streamer, [])
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
