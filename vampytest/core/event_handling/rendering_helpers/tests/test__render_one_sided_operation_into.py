from scarletio import DEFAULT_ANSI_HIGHLIGHTER, HIGHLIGHT_TOKEN_TYPES

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..assertion_rendering import _render_one_sided_operation_into


def _iter_options():
    yield (
        [
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'bool'),
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('),
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'),
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'),
        ],
        None,
        'operation = bool(value)\n',
    )
    
    # with highlighter
    yield (
        [
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'bool'),
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('),
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'),
            (HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'),
        ],
        DEFAULT_ANSI_HIGHLIGHTER,
        'operation = bool(value)\n',
    )


@_(call_from(_iter_options()).returning_last())
def test__render_one_sided_operation_into(operation, highlighter):
    """
    Tests whether ``_render_one_sided_operation_into`` works as intended.
    
    Parameters
    ----------
    operation : `str`
        The whole operation to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    into = _render_one_sided_operation_into(operation, highlighter, [])
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
