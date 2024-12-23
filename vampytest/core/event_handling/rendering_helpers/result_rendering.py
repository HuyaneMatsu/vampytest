__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES, add_highlighted_part_into

from .report_rendering import render_failure_report_into, render_output_output_into
from .result_rendering_common import render_test_header_into


def render_result_reversed_into(result, highlighter, into):
    """
    Creates a reversed failure message for the given test handle.
    
    Parameters
    ----------
    result : ``Result``
        Test result.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
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
        highlighter,
        into,
    )


def render_result_wrapper_conflict_into(result, highlighter, into):
    """
    Renders wrapper conflict.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
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
        highlighter,
        into,
    )
    
    wrapper_conflict = result.wrapper_conflict
    reason = wrapper_conflict.reason
    if (reason is not None):
        into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, 'Reason: ', highlighter, into)
        into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_POSITIVE, reason, highlighter, into)
        into.append('\n')
    
    into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, 'Between wrapper(s):', highlighter, into)
    into.append('\n')
    into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX, '-', highlighter, into)
    into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, into)
    into.append(repr(wrapper_conflict.wrapper_0))
    into.append('\n')
    
    wrapper_1 = wrapper_conflict.wrapper_1
    if (wrapper_1 is not None):
        into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX, '-', highlighter, into)
        into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, into)
        into.append(repr(wrapper_1))
        into.append('\n')
    
    return into


def render_result_failure_report_into(result, highlighter, into):
    return render_failure_report_into(
        result.get_failure_report(),
        result.case.path_parts,
        result.case.name,
        result.handle.get_test_documentation_lines(),
        result.handle.final_call_state,
        result.get_output_report(),
        highlighter,
        into,
    )


def render_result_failing_into(result, highlighter, into):
    if result.is_conflicted():
        renderer = render_result_wrapper_conflict_into
    elif result.reversed:
        renderer = render_result_reversed_into
    else:
        renderer = render_result_failure_report_into
    
    return renderer(result, highlighter, into)


def render_result_informal_into(result, highlighter, into):
    output_report = result.get_output_report()
    if (output_report is not None):
        into = render_output_output_into(
            output_report, 
            result.case.path_parts,
            result.case.name,
            result.handle.get_test_documentation_lines(),
            result.handle.final_call_state,
            highlighter,
            into,
        )
    
    return into
