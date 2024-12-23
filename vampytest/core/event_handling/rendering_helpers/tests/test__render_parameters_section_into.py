from scarletio import DEFAULT_ANSI_HIGHLIGHTER

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..result_rendering_common import render_parameters_section_into


def _iter_options():
    # Default
    yield (
        'Parameters:',
        None,
        None,
        None,
        (
            '\n'
            'Parameters: N/A\n'
        ),
    )
    
    # positionals
    yield (
        'Parameters:',
        [12, 'mister'],
        None,
        None,
        (
            '\n'
            'Parameters:\n'
            '    12\n'
            '    \'mister\'\n'
        ),
    )
    
    # keywords
    yield (
        'Parameters:',
        None,
        {'hey': 12, 'mister': 'sister'},
        None,
        (
            '\n'
            'Parameters:\n'
            '    hey = 12\n'
            '    mister = \'sister\'\n'
        ),
    )
    
    # positional + keywords
    yield (
        'Parameters:',
        [12, 'mister'],
        {'hey': 12, 'mister': 'sister'},
        None,
        (
            '\n'
            'Parameters:\n'
            '    12\n'
            '    \'mister\'\n'
            '    hey = 12\n'
            '    mister = \'sister\'\n'
        ),
    )
    
    # Highlighted
    yield (
        'Parameters:',
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            '\n'
            'Parameters: N/A\n'
        ),
    )


@_(call_from(_iter_options()).returning_last())
def test__render_parameters_section_into(title, positional_parameters, keyword_parameters, highlighter):
    """
    Tests whether ``render_parameters_section_into`` works as intended.
    
    Parameters
    ----------
    title : `str`
        Section title.
    
    positional_parameters : `None | list<object>`
        Positional parameters passed to the test.
    
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters passed to the test.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    into = render_parameters_section_into(title, positional_parameters, keyword_parameters, highlighter, [])
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
