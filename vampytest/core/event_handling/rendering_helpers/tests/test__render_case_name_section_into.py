from scarletio import DEFAULT_ANSI_HIGHLIGHTER

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
    into = render_case_name_section_into(name, highlighter, [])
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
