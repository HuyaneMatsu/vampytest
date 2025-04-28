from scarletio import (
    DEFAULT_ANSI_HIGHLIGHTER, HIGHLIGHT_TOKEN_TYPES, get_highlight_streamer, iter_split_ansi_format_codes
)

from ....assertions import assert_eq, assert_instance
from ....handling.call_state import CallState
from ....utils import _
from ....wrappers import call_from

from ..result_rendering_common import render_test_header_into


def _iter_options():
    # default
    yield (
        'Hey mister',
        ('here', 'there'),
        'this',
        None,
        None,
        None,
        (
            'Hey mister at: here.there:this\n'
        ),
    )
    
    # no path_parts
    yield (
        'Hey mister',
        (),
        'this',
        None,
        None,
        None,
        (
            'Hey mister at: this\n'
        ),
    )
    
    # with documentation
    yield (
        'Hey mister',
        ('here', 'there'),
        'this',
        ['for nyanner in nyanners:', '    nyanner.nyan()'],
        None,
        None,
        (
            'Hey mister at: here.there:this\n'
            '\n'
            '> for nyanner in nyanners:\n'
            '>     nyanner.nyan()\n'
        ),
    )
    
    # with call state (parameters)
    yield (
        'Hey mister',
        ('here', 'there'),
        'this',
        None,
        CallState().with_parameters([12], {'mister': int}),
        None,
        (
            'Hey mister at: here.there:this\n'
            '\n'
            'Parameters:\n'
            '    12\n'
            '    mister = int\n'
        ),
    )
    
    # with call state (named)
    yield (
        'Hey mister',
        ('here', 'there'),
        'this',
        None,
        CallState().with_name('koishi'),
        None,
        (
            'Hey mister at: here.there:this\n'
            '\n'
            'Named: koishi\n'
        ),
    )
    
    # with highlighter
    yield (
        'Hey mister',
        ('here', 'there'),
        'this',
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Hey mister at: here.there:this\n'
        ),
    )


@_(call_from(_iter_options()).returning_last())
def test__render_test_header_into(title, path_parts, name, documentation_lines, call_state, highlighter):
    """
    Tests whether ``render_test_header_into`` works as intended.
    
    Parameters
    ----------
    title : `str`
        The title to add.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    highlight_streamer = get_highlight_streamer(highlighter)
    
    into = render_test_header_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        title,
        path_parts,
        name,
        documentation_lines,
        call_state,
        highlight_streamer,
        [],
    )
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
