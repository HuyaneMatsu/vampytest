from scarletio import HIGHLIGHT_TOKEN_TYPES

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
    into = _render_two_sided_operation_into(operation, highlighter, [])
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
