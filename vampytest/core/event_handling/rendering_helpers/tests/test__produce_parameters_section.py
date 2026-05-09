from scarletio import DEFAULT_ANSI_HIGHLIGHTER, get_highlight_streamer, iter_split_ansi_format_codes

from ....assertions import assert_eq, assert_instance
from ....utils import _
from ....wrappers import call_from

from ..result_rendering_common import produce_parameters_section


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
def test__produce_parameters_section(title, positional_parameters, keyword_parameters, highlighter):
    """
    Tests whether ``produce_parameters_section`` works as intended.
    
    Parameters
    ----------
    title : `str`
        Section title.
    
    positional_parameters : `None | list<object>`
        Positional parameters passed to the test.
    
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters passed to the test.
    
    highlighter : ``None | HighlightFormatterContext``
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    highlight_streamer = get_highlight_streamer(highlighter)
    output = []
    for item in produce_parameters_section(title, positional_parameters, keyword_parameters):
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
