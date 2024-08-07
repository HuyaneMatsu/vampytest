__all__ = ()

from os import get_terminal_size

from scarletio import DEFAULT_ANSI_HIGHLIGHTER, render_exception_into

from ...environment.default import __file__ as VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH
from ...environment.scarletio_coroutine import __file__ as VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH

from ..colors import COLOR_FAIL, COLOR_PATH, COLOR_SKIP
from ..default_output_writer import DEFAULT_BREAK_LINE_LENGTH
from ..text_styling import style_text_block, style_text_into


def create_break(character):
    """
    Creates a break with the given character.
    
    Parameters
    ----------
    character : `str`
        The character to create the break from.
    
    Returns
    -------
    break : `str`
    """
    try:
        terminal_size = get_terminal_size()
    except OSError:
        break_line_length = DEFAULT_BREAK_LINE_LENGTH
    else:
        break_line_length = terminal_size.columns

    return character * break_line_length


def render_route_parts_into(into, result):
    """
    Adds route parts into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    result : ``Result``
        Test result to get its path of.
    
    Returns
    -------
    into : `list` of `str`
    """
    case = result.handle.case
    
    into.append(case.import_route)
    into.append(':')
    into.append(case.name)
    
    return into


def render_documentation_into(into, result):
    """
    Adds the documentation into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    result : ``Result``
        Test result to get its path of.
    
    Returns
    -------
    into : `list` of `str`
    """
    documentation = result.handle.get_test_documentation()
    if (documentation is not None):
        into.append('\n')
        into.append(documentation)
    
    return into


def render_test_position_into(into, title, title_format_code, result):
    """
    Renders the test's position into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    title : `str`
        Title to color.
    title_format_code : `str`
        Format code to format the title.
    result : ``Result``
        Test result to get its path of.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = style_text_into(into, title, title_format_code)
    into.append(' at: ')
    for _ in style_text_block(into, COLOR_PATH):
        into = render_route_parts_into(into, result)
    
    render_documentation_into(into, result)
    return into


def render_parameters_into(into, positional_parameters, keyword_parameters):
    """
    Renders the input parameters of to the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    positional_parameters : `None`, `list<object>`
        Positional parameters passed to the test.
    keyword_parameters : `None`, `dict<str, object>`
        Keyword parameters passed to the test.
    
    Returns
    -------
    into : `list` of `str`
    """
    if (positional_parameters is not None):
        for parameter_value in positional_parameters:
            into.append('\n    ')
            into.append(repr(parameter_value))
    
    
    if (keyword_parameters is not None):
        for (parameter_name, parameter_value) in keyword_parameters.items():
            into.append('\n    ')
            into.append(parameter_name)
            into.append(' = ')
            into.append(repr(parameter_value))
    
    if (positional_parameters is None) and (keyword_parameters is None):
        into.append(' N/A')
    
    return into


def maybe_render_parameters_section_into(into, result):
    """
    Renders the parameters section into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    result : ``Result``
        Test result.
    
    Returns
    -------
    into : `list` of `str`
    """
    final_call_state = result.handle.final_call_state
    if (final_call_state is not None) and final_call_state:
        into.append('\n\nParameters:')
        into = render_parameters_into(into, final_call_state.positional_parameters, final_call_state.keyword_parameters)
    
    return into


def maybe_render_output_into(into, result):
    """
    Renders the captured output section into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    result : ``Result``
        Test result.
    
    Returns
    -------
    into : `list` of `str`
    """
    report = result.get_output_report()
    if (report is not None):
        if into and (not into[-1].endswith('\n')):
            into.append('\n')
        
        into.append('\nCaptured output while running the test:\n')
        into.append(create_break('-'))
        into.append('\n')
        into.append(report.output)
    
    return into


def render_report_reversed_into(into, result):
    """
    Creates a reversed failure message for the given test handle.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    result : ``Result``
        Test result.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = render_test_position_into(into, 'Reversed test passed', COLOR_FAIL, result)
    
    final_call_state = result.handle.final_call_state
    if (final_call_state is not None) and final_call_state:
        into.append('\nParameters: ')
        into = render_parameters_into(into, final_call_state.positional_parameters, final_call_state.keyword_parameters)
    
    return into


def render_wrapper_conflict_into(into, result):
    """
    Renders wrapper conflict.
    
    Parameter
    ---------
    into : `list` of `str`
        List to render into.
    result : ``Result``
        The result failing with wrapper conflict.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = render_test_position_into(into, 'Wrapper conflict', COLOR_FAIL, result)
    
    wrapper_conflict = result.wrapper_conflict
    reason = wrapper_conflict.reason
    if (reason is not None):
        into.append('\nReason: ')
        into = style_text_into(into, reason, COLOR_FAIL)
    
    into.append('\nBetween wrapper(s):\n- ')
    into.append(repr(wrapper_conflict.wrapper_0))
    
    wrapper_1 = wrapper_conflict.wrapper_1
    if (wrapper_1 is not None):
        into.append('\n- ')
        into.append(repr(wrapper_1))
    
    return into


def ignore_invoke_test_frame(frame):
    """
    Ignores the frame where the test is called from.
    
    Parameters
    ----------
    frame : ``FrameProxyBase``
        The frame to check.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    file_name = frame.file_name
    name = frame.name
    line = frame.line
    
    if file_name == VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH:
        if name == 'run':
            if line == 'returned_value = test(*positional_parameters, **keyword_parameters)':
                should_show_frame = False
    
    elif file_name == VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH:
        if name == '_run_async':
            if line == 'returned_value = await test(*positional_parameters, **keyword_parameters)':
                should_show_frame = False
    
    return should_show_frame


def render_report_asserting_into(into, result, report):
    """
    Renders assertion failure report.
    
    Parameter
    ---------
    into : `list` of `str`
        List to render into.
    result : ``Result``
        The ran test.
    report : ``ReportFailureAsserting``
        Report containing the failure information.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = render_test_position_into(into, 'Assertion failed', COLOR_FAIL, result)
    maybe_render_parameters_section_into(into, result)
    into.append('\n')
    into = report.assertion_exception.render_failure_message_parts_into(into)
    into = maybe_render_output_into(into, result)
    return into


def render_report_raising_into(into, result, report):
    """
    Renders raising failure report.
    
    Parameter
    ---------
    into : `list` of `str`
        List to render into.
    result : ``Result``
        The ran test.
    report : ``ReportFailureRaising``
        Report containing the failure information.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = render_test_position_into(into, 'Unexpected exception', COLOR_FAIL, result)
    maybe_render_parameters_section_into(into, result)
    into.append('\n')
    
    expected_exceptions = report.expected_exceptions
    if expected_exceptions is not None:
        into.append('\nExpected exceptions: ')
        
        exception_added = False
        
        for expected_exception in expected_exceptions:
            if exception_added:
                into.append(', ')
            else:
                exception_added = True
            
            if isinstance(expected_exception, type):
                expected_exception_representation = expected_exception.__name__
            else:
                expected_exception_representation = repr(expected_exception)
            
            into.append(expected_exception_representation)
        
        into.append('\nAccept sub-types: ')
        into.append('true' if report.accept_subtypes else 'false')
    
    
    exception_received = report.exception_received
    if (exception_received is not None):
        into.append('\n')
        into.append(create_break('-'))
        into.append('\n')
        
        render_exception_into(
            exception_received,
            into,
            filter = ignore_invoke_test_frame,
            highlighter = DEFAULT_ANSI_HIGHLIGHTER
        )
    
    into = maybe_render_output_into(into, result)
    return into


def render_report_returning_into(into, result, report):
    """
    Renders returning failure report.
    
    Parameter
    ---------
    into : `list` of `str`
        List to render into.
    result : ``Result``
        The ran test.
    report : ``ReportFailureReturning``
        Report containing the failure information.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = render_test_position_into(into, 'Unexpected return', COLOR_FAIL, result)
    maybe_render_parameters_section_into(into, result)
    
    into.append('\n\nExpected return: ')
    into.append(repr(report.expected_value))
    
    into.append('\nReceived return: ' )
    into.append(repr(report.received_value))
    
    into = maybe_render_output_into(into, result)
    return into


def render_report_output_into(into, result, report):
    """
    Renders output report.
    
    Parameter
    ---------
    into : `list` of `str`
        List to render into.
    result : ``Result``
        The ran test.
    report : ``ReportOutput``
        Report containing the output.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = render_test_position_into(into, 'Output captured', COLOR_SKIP, result)
    maybe_render_parameters_section_into(into, result)
    
    into.append('\n')
    into.append(create_break('-'))
    into.append('\n')
    into.append(report.output)
    
    return into


def render_function_parameters_into(into, parameters):
    """
    Renders a function's parameters.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    parameters : `list<Parameter>`
        The parameter to render.
    
    Returns
    -------
    into : `list<str>`
    """
    previous = None
    
    for parameter in parameters:
        if previous is not None:
            if previous.is_positional_only():
                if parameter.is_keyword_only():
                    into.append('\n    /\n    *')
                elif (not parameter.is_positional_only()):
                    into.append('\n    /')
            
            elif previous.is_positional():
                if parameter.is_keyword_only():
                    into.append('\n    *')
        
        into.append('\n    ')
        
        # * or ** ?
        if parameter.is_args():
            into.append('*')
        elif parameter.is_kwargs():
            into.append('**')
        
        # name
        into.append(parameter.name)
        
        # default
        if parameter.has_default:
            into.append(' = ')
            into.append(repr(parameter.default))
        
        previous = parameter
    
    return into


def render_unsatisfied_parameters_into(issue_parts, unsatisfied_parameters):
    """
    Renders the unsatisfied parameters.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    parameters : `list<Parameter>`
        The parameter to render.
    
    Returns
    -------
    into : `list<str>`
    """
    for parameter in unsatisfied_parameters:
        issue_parts.append('\n    ')
        issue_parts.append(parameter.name)
    
    return issue_parts


def render_extra_parameters_into(issue_parts, extra_positional_parameters, extra_keyword_parameters):
    if (extra_positional_parameters is not None):
        for parameter_value in extra_positional_parameters:
            issue_parts.append('\n    ')
            issue_parts.append(repr(parameter_value))
    
    if (extra_keyword_parameters is not None):
        for parameter_name, parameter_value in extra_keyword_parameters:
            issue_parts.append('\n    ')
            issue_parts.append(parameter_name)
            issue_parts.append(' = ')
            issue_parts.append(repr(parameter_value))
    
    return issue_parts


def render_report_parameter_mismatch_into(into, result, report):
    """
    Renders parameter mismatch failure report.
    
    Parameter
    ---------
    into : `list` of `str`
        List to render into.
    result : ``Result``
        The ran test.
    report : ``ReportFailureParameterMismatch``
        Report containing the failure information.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = render_test_position_into(into, 'Parameter mismatch', COLOR_FAIL, result)
    parameter_mismatch = report.parameter_mismatch
    
    into.append('\n\nFunction parameters:')
    into = render_function_parameters_into(into, parameter_mismatch.parameters)
    
    into.append('\n\nGiven Parameters:')
    into = render_parameters_into(into, parameter_mismatch.positional_parameters, parameter_mismatch.keyword_parameters)
    
    unsatisfied_parameters = parameter_mismatch.unsatisfied_parameters
    if (unsatisfied_parameters is not None):
        into.append('\n\nUnsatisfied function parameters:')
        into = render_unsatisfied_parameters_into(into, unsatisfied_parameters)
    
    extra_positional_parameters = parameter_mismatch.extra_positional_parameters
    extra_keyword_parameters = parameter_mismatch.extra_keyword_parameters
    if (extra_positional_parameters is not None) or (extra_keyword_parameters is not None):
        into.append('\n\nExtra parameters:')
        into = render_parameters_into(into, extra_positional_parameters, extra_keyword_parameters)
    
    return into
