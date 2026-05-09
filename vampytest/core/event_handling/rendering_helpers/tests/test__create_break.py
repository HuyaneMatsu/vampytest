from os import terminal_size as TerminalSize

from ....assertions import assert_instance
from ....mocking import mock_globals
from ....utils import _
from ....wrappers import call_from

from ...default_output_writer import DEFAULT_BREAK_LINE_LENGTH

from ..result_rendering_common import create_break


def _iter_options():
    yield '-', None, '-' * DEFAULT_BREAK_LINE_LENGTH
    yield '-', 12, '-' * 12


@_(call_from(_iter_options()).returning_last())
def test__create_break(character, terminal_width):
    """
    Tests whether ``create_break`` works as intended.
    
    Parameters
    ----------
    character : `str`
        The character to create the break from.
    
    terminal_width : `None | int`
        The terminal's width to return.
    
    Returns
    -------
    output : `str`
    """
    def get_terminal_size_mock():
        nonlocal terminal_width
        if (terminal_width is None):
            raise OSError
        
        return TerminalSize((terminal_width, 0))
    
    mocked = mock_globals(
        create_break,
        get_terminal_size = get_terminal_size_mock,
    )
    
    output = mocked(character)
    
    assert_instance(output, str)
    
    return output
