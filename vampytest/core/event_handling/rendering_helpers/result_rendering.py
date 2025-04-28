__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES

from .report_rendering import render_failure_report_into, render_output_output_into
from .result_rendering_common import render_test_header_into


def render_result_reversed_into(result, highlight_streamer, into):
    """
    Creates a reversed failure message for the given test handle.
    
    Parameters
    ----------
    result : ``Result``
        Test result.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list<str>`
    """
    return render_test_header_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        'Reversed test passed',
        result.case.path_parts,
        result.case.name,
        result.handle.get_test_documentation_lines(),
        result.handle.final_call_state,
        highlight_streamer,
        into,
    )


def render_result_wrapper_conflict_into(result, highlight_streamer, into):
    """
    Renders wrapper conflict.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        List to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    into = render_test_header_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        'Wrapper conflict', 
        result.case.path_parts,
        result.case.name,
        result.handle.get_test_documentation_lines(),
        None,
        highlight_streamer,
        into,
    )
    
    wrapper_conflict = result.wrapper_conflict
    reason = wrapper_conflict.reason
    if (reason is not None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE,
            'Reason: ',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_POSITIVE,
            reason,
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
    
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE,
       'Between wrapper(s):',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX,
        '-',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
        ' ',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT,
        repr(wrapper_conflict.wrapper_0),
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    
    wrapper_1 = wrapper_conflict.wrapper_1
    if (wrapper_1 is not None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX,
            '-',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
            ' ',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT,
            repr(wrapper_conflict.wrapper_1),
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
    
    return into


def render_result_failure_report_into(result, highlight_streamer, into):
    """
    Renders a failure report.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        List to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    return render_failure_report_into(
        result.get_failure_report(),
        result.case.path_parts,
        result.case.name,
        result.handle.get_test_documentation_lines(),
        result.handle.final_call_state,
        result.get_output_report(),
        highlight_streamer,
        into,
    )


def render_result_failing_into(result, highlight_streamer, into):
    """
    Renders a failing result.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        List to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    if result.is_conflicted():
        renderer = render_result_wrapper_conflict_into
    elif result.reversed:
        renderer = render_result_reversed_into
    else:
        renderer = render_result_failure_report_into
    
    return renderer(result, highlight_streamer, into)


def render_result_informal_into(result, highlight_streamer, into):
    """
    Renders an informal result.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        List to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    output_report = result.get_output_report()
    if (output_report is not None):
        into = render_output_output_into(
            output_report, 
            result.case.path_parts,
            result.case.name,
            result.handle.get_test_documentation_lines(),
            result.handle.final_call_state,
            highlight_streamer,
            into,
        )
    
    return into
