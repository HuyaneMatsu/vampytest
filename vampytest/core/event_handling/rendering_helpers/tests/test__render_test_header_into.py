from scarletio import DEFAULT_ANSI_HIGHLIGHTER, HIGHLIGHT_TOKEN_TYPES

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
    
    # with call state
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
    into = render_test_header_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        title,
        path_parts,
        name,
        documentation_lines,
        call_state,
        highlighter,
        [],
    )
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
