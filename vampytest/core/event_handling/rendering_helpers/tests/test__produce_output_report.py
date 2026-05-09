from scarletio import DEFAULT_ANSI_HIGHLIGHTER, get_highlight_streamer, iter_split_ansi_format_codes

from ....assertions import assert_eq, assert_instance
from ....handling import CallState
from ....result import ReportOutput
from ....utils import _
from ....wrappers import call_from

from ..report_rendering import produce_output_report
from ..result_rendering_common import create_break


def _iter_options():
    # Default
    yield (
        ReportOutput('hello\nnyanner'),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        (
            'Captured output at: good.pear:test__function\n'
            '----\n'
            'hello\n'
            'nyanner\n'
        ),
    )
    
    # with documentation & call state
    yield (
        ReportOutput('hello\nnyanner'),
        ('good', 'pear'),
        'test__function',
        [
            'Code that',
            'Does things'
        ],
        CallState().with_parameters([int], None),
        None,
        (
            'Captured output at: good.pear:test__function\n'
            '\n'
            '> Code that\n'
            '> Does things\n'
            '\n'
            'Parameters:\n'
            '    int\n'
            '----\n'
            'hello\n'
            'nyanner\n'
        ),
    )
    
    # with highlighter
    yield (
        ReportOutput('hello\nnyanner'),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Captured output at: good.pear:test__function\n'
            '----\n'
            'hello\n'
            'nyanner\n'
        ),
    )


@_(call_from(_iter_options()).returning_last())
def test__produce_output_report(report, path_parts, name, documentation_lines, call_state, highlighter):
    """
    Tests whether ``produce_output_report`` works as intended.
    
    Parameters
    ----------
    report : ``ReportOutput``
        Report containing the output.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : ``None | CallState``
        Call state of the report.
    
    highlighter : ``None | HighlightFormatterContext``
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    def create_break_mock(character):
        return character * 4
    
    highlight_streamer = get_highlight_streamer(highlighter)
    create_break_code_original = create_break.__code__
    output = []
    
    try:
        create_break.__code__ = create_break_mock.__code__
        
        for item in produce_output_report(report, path_parts, name, documentation_lines, call_state):
            output.extend(highlight_streamer.asend(item))
    finally:
        create_break.__code__ = create_break_code_original
    
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
