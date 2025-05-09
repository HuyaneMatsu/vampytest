__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES
from scarletio.utils.trace.frame_proxy import get_exception_frames
from scarletio.utils.trace.trace import _render_exception_into, _render_frames_into

from ...assertions import AssertionRaising
from ...assertions.exception import _ignore_assertion_frames
from ...environment.default import __file__ as VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH
from ...environment.scarletio_coroutine import __file__ as VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH
from ...result import (
    ReportFailureAsserting, ReportFailureParameterMismatch, ReportFailureRaising, ReportFailureReturning
)

from .assertion_rendering import render_assertion_into
from .parameter_rendering import (
    _produce_assignation, _produce_value_representation, _render_bool_non_default_into,
    _render_parameter_representation_into, _render_types_parameter_representation_into
)
from .result_rendering_common import (
    create_break, render_case_name_section_into, render_parameters_section_into, render_test_header_into
)


def _render_break_and_output(separator_token_type, output, highlight_streamer, into):
    """
    Renders a break line and the given output.
    
    Parameters
    ----------
    separator_token_type : `int`
        Token type identifier for the separator line.
    
    output : `str`
        Output to render.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        List to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    into.extend(highlight_streamer.asend((
        separator_token_type,
        create_break('-'),
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT,
       output,
    )))
    if not output.endswith('\n'):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
    
    return into
    

def render_output_output_into(report, path_parts, name, documentation_lines, call_state, highlight_streamer, into):
    """
    Renders output report.
    
    Parameter
    ---------
    report : ``ReportOutput``
        Report containing the output.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state of the report.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        List to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    into = render_test_header_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEUTRAL,
        'Captured output', 
        path_parts,
        name,
        documentation_lines,
        call_state,
        highlight_streamer,
        into,
    )
    into = _render_break_and_output(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEUTRAL, report.output, highlight_streamer, into
    )
    return into


def _maybe_render_output_report_into(report, highlight_streamer, into):
    """
    Renders the captured output report as a section into the given list.
    
    Parameters
    ----------
    report : ``ReportOutput``
        The report to render.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list<str>`
    """
    if (report is not None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE,
           'Captured output while running the test:',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        into = _render_break_and_output(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, report.output, highlight_streamer, into
        )
    
    return into


def _render_report_asserting_into(
    report, path_parts, name, documentation_lines, call_state, output_report, highlight_streamer, into
):
    """
    Renders assertion failure report.
    
    Parameter
    ---------
    report : ``ReportFailureAsserting``
        Report containing the failure information.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state of the report.
    
    output_report : `None | ReportOutput`
        Output report if any.
    
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
        'Assertion failed',
        path_parts,
        name,
        documentation_lines,
        call_state,
        highlight_streamer,
        into,
    )
    
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    assertion_exception = report.assertion_exception
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_TITLE,
        'Assertion traceback (most recent call last):',    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    into = _render_frames_into(
        get_exception_frames(assertion_exception),
        _ignore_assertion_frames,
        highlight_streamer,
        into,
    )
    
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    into = render_assertion_into(assertion_exception.assertion, highlight_streamer, into)
    
    assertion = assertion_exception.assertion
    if isinstance(assertion, AssertionRaising):
        received_exception = assertion.received_exception
        if (received_exception is not None):
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
                '\n',
            )))
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
                'Captured exception failing the assertion:',
            )))
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
                '\n',
            )))
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
                create_break('-'),            )))
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
                '\n',
            )))
            into = _render_exception_into(
                received_exception,
                None,
                highlight_streamer,
                into,
            )
    
    exception = assertion.exception
    if (exception is not None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
            'Unexpected exception occurred withing the assertion:',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
            create_break('-'),        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        into = _render_exception_into(
            exception,
            None,
            highlight_streamer,
            into,
        )
    
    into = _maybe_render_output_report_into(output_report, highlight_streamer, into)
    return into


def _render_function_parameters_into(parameters, highlight_streamer, into):
    """
    Renders a function's parameters.
    
    Parameters
    ----------
    parameters : `list<Parameter>`
        The parameter to render.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        Container to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    previous = None
    
    for parameter in parameters:
        if (previous is not None):
            if previous.is_positional_only() and (not parameter.is_positional_only()):
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
                    '    ',
                )))
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR,
                    '/',
                )))
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
                    '\n',
                )))
            
            if previous.is_positional() and parameter.is_keyword_only():
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
                    '    ',
                )))
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR,
                    '*',
                )))
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
                    '\n',
                )))
        
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
            '    ',
        )))
        
        # * or ** ?
        if parameter.is_args():
            prefix = '*'
        elif parameter.is_kwargs():
            prefix = '**'
        else:
            prefix = None
        
        if (prefix is not None):
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR,
                prefix,
            )))
        
        # name
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE,
            parameter.name,
        )))
        
        # default
        if parameter.has_default:
            for item in _produce_assignation():
                into.extend(highlight_streamer.asend(item))
            for item in _produce_value_representation(parameter.default):
                into.extend(highlight_streamer.asend(item))
        
        previous = parameter
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
    
    return into


def _render_unsatisfied_parameters_into(unsatisfied_parameters, highlight_streamer, into):
    """
    Renders the unsatisfied parameters.
    
    Parameters
    ----------
    unsatisfied_parameters : `list<Parameter>`
        The parameter to render.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        Container to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    for parameter in unsatisfied_parameters:
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
            '    ',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE,
            parameter.name,
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
    
    return into


def _render_report_parameter_mismatch_into(
    report, path_parts, name, documentation_lines, call_state, output_report, highlight_streamer, into
):
    """
    Renders parameter mismatch failure report.
    
    Parameter
    ---------
    report : ``ReportFailureParameterMismatch``
        Report containing the failure information.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state of the report.
    
    output_report : `None | ReportOutput`
        Output report if any.
    
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
        'Parameter mismatch', 
        path_parts,
        name,
        documentation_lines,
        None,
        highlight_streamer,
        into,
    )
    
    # Since we do not wanna render the parameters in the header, we pass the call state there as `None`
    # and then we render the case name section separately.
    if (call_state is not None):
        case_name = call_state.name
        if (case_name is not None):
            into = render_case_name_section_into(case_name, highlight_streamer, into)
    
    parameter_mismatch = report.parameter_mismatch
    
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE,
        'Function parameters:',
    )))
    into = _render_function_parameters_into(
        parameter_mismatch.parameters,
        highlight_streamer,
        into,
    )
    
    into = render_parameters_section_into(
        'Given parameters:',
        parameter_mismatch.positional_parameters,
        parameter_mismatch.keyword_parameters,
        highlight_streamer,
        into
    )
    
    
    unsatisfied_parameters = parameter_mismatch.unsatisfied_parameters
    if (unsatisfied_parameters is not None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE,
            'Unsatisfied function parameters:'
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        into = _render_unsatisfied_parameters_into(
            unsatisfied_parameters,
            highlight_streamer,
            into,
        )
    
    extra_positional_parameters = parameter_mismatch.extra_positional_parameters
    extra_keyword_parameters = parameter_mismatch.extra_keyword_parameters
    if (extra_positional_parameters is not None) or (extra_keyword_parameters is not None):
        into = render_parameters_section_into(
            'Extra parameters:',
            extra_positional_parameters,
            extra_keyword_parameters,
            highlight_streamer,
            into,
        )
    
    return into


def _ignore_invoke_test_frame(frame):
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


def _render_report_raising_into(
    report, path_parts, name, documentation_lines, call_state, output_report, highlight_streamer, into
):
    """
    Renders raising failure report.
    
    Parameter
    ---------
    report : ``ReportFailureRaising``
        Report containing the failure information.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state of the report.
    
    output_report : `None | ReportOutput`
        Output report if any.
    
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
        ('Missing exception' if report.exception_received is None else 'Unexpected exception'),
        path_parts,
        name,
        documentation_lines,
        call_state,
        highlight_streamer,
        into,
    )
    
    expected_exceptions = report.expected_exceptions
    if (expected_exceptions is not None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        into = _render_types_parameter_representation_into(
            'expected_exceptions', expected_exceptions, highlight_streamer, into
        )
        into = _render_bool_non_default_into(
            'accept_subtypes', report.accept_subtypes, True, highlight_streamer, into
        )
    
    
    exception_received = report.exception_received
    if (exception_received is not None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
            create_break('-'),        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        
        into = _render_exception_into(
            exception_received,
            _ignore_invoke_test_frame,
            highlight_streamer,
            into,
        )
    
    into = _maybe_render_output_report_into(output_report, highlight_streamer, into)
    return into


def _render_report_returning_into(
    report, path_parts, name, documentation_lines, call_state, output_report, highlight_streamer, into
):
    """
    Renders returning failure report.
    
    Parameter
    ---------
    report : ``ReportFailureReturning``
        Report containing the failure information.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state of the report.
    
    output_report : `None | ReportOutput`
        Output report if any.
    
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
        'Unexpected return',
        path_parts,
        name,
        documentation_lines,
        call_state,
        highlight_streamer,
        into,
    )
    
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    into = _render_parameter_representation_into('expected_return', report.expected_value, highlight_streamer, into)
    into = _render_parameter_representation_into('received_return', report.received_value, highlight_streamer, into)
    
    into = _maybe_render_output_report_into(output_report, highlight_streamer, into)
    return into


def _render_report_unknown_failure_into(
    report, path_parts, name, documentation_lines, call_state, output_report, highlight_streamer, into
):
    """
    Renders an unknown failure report.
    
    Parameter
    ---------
    report : ``ReportBase``
        Report containing the failure information.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state of the report.
    
    output_report : `None | ReportOutput`
        Output report if any.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        List to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    into = render_test_header_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_UNKNOWN,
        type(report).__name__,
        path_parts,
        name,
        documentation_lines,
        call_state,
        highlight_streamer,
        into,
    )
    
    into = _maybe_render_output_report_into(output_report, highlight_streamer, into)
    return into


FAILURE_REPORT_RENDERERS = {
    ReportFailureAsserting: _render_report_asserting_into,
    ReportFailureParameterMismatch: _render_report_parameter_mismatch_into,
    ReportFailureRaising: _render_report_raising_into,
    ReportFailureReturning: _render_report_returning_into,
}


def render_failure_report_into(
    report, path_parts, name, documentation_lines, call_state, output_report, highlight_streamer, into
):
    """
    Renders the given failure report.
    
    Parameters
    ----------
    report : ``ReportBase``
        The report to render.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state of the report.
    
    output_report : `None | ReportOutput`
        Output report if any.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        List to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    return FAILURE_REPORT_RENDERERS.get(type(report), _render_report_unknown_failure_into)(
        report, path_parts, name, documentation_lines, call_state, output_report, highlight_streamer, into
    )
