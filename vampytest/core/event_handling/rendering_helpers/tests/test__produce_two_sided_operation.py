from scarletio import HIGHLIGHT_TOKEN_TYPES, get_highlight_streamer, iter_split_ansi_format_codes

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..assertion_rendering import _produce_two_sided_operation


def _iter_options():
    yield (
        [
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '+'),
        ],
        None,
        'operation = value_0 + value_1\n',
    )


@_(call_from(_iter_options()).returning_last())
def test__produce_two_sided_operation(operation, highlighter):
    """
    Tests whether ``_produce_two_sided_operation`` works as intended.
    
    Parameters
    ----------
    operation : `str`
        The operation between the two sides.
    
    highlighter : ``None | HighlightFormatterContext``
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    highlight_streamer = get_highlight_streamer(highlighter)
    output = []
    
    for item in _produce_two_sided_operation(operation):
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
