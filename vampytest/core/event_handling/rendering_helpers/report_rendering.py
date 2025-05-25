__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES
from scarletio.utils.trace.frame_proxy import get_exception_frames
from scarletio.utils.trace.trace import _produce_exception, _produce_frames

from ...assertions import AssertionRaising
from ...assertions.exception import _ignore_assertion_frames
from ...environment.default import __file__ as VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH
from ...environment.scarletio_coroutine import __file__ as VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH
from ...result import (
    ReportFailureAsserting, ReportFailureParameterMismatch, ReportFailureRaising, ReportFailureReturning
)

from .assertion_rendering import produce_assertion
from .parameter_rendering import (
    _produce_assignation, _produce_value_representation, _produce_bool_non_default,
    _produce_parameter_representation, _produce_types_parameter_representation
)
from .result_rendering_common import (
    create_break, produce_case_name_section, produce_parameters_section, produce_test_header
)


def _produce_break_and_output(separator_token_type, output):
    """
    Renders a break line and the given output.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    separator_token_type : `int`
        Token type identifier for the separator line.
    
    output : `str`
        Output to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield separator_token_type, create_break('-')
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT, output
    if not output.endswith('\n'):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    

def produce_output_report(report, path_parts, name, documentation_lines, call_state):
    """
    Renders output report.
    
    This functions is an iterable generator.
    
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
    
    call_state : ``None | CallState``
        Call state of the report.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from produce_test_header(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEUTRAL,
        'Captured output', 
        path_parts,
        name,
        documentation_lines,
        call_state,
    )
    yield from _produce_break_and_output(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEUTRAL, report.output)


def _maybe_produce_output_report(report):
    """
    Renders the captured output report as a section into the given list.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    report : ``ReportOutput``
        The report to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    if (report is not None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, 'Captured output while running the test:'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield from  _produce_break_and_output(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, report.output)


def _produce_report_asserting(report, path_parts, name, documentation_lines, call_state, output_report):
    """
    Renders assertion failure report.
    
    This functions is an iterable generator.
    
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
    
    call_state : ``None | CallState``
        Call state of the report.
    
    output_report : ``None | ReportOutput``
        Output report if any.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from produce_test_header(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        'Assertion failed',
        path_parts,
        name,
        documentation_lines,
        call_state,
    )
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    
    assertion_exception = report.assertion_exception
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_TITLE, 'Assertion traceback (most recent call last):'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    yield from _produce_frames(get_exception_frames(assertion_exception), _ignore_assertion_frames)
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    yield from produce_assertion(assertion_exception.assertion)
    
    assertion = assertion_exception.assertion
    if isinstance(assertion, AssertionRaising):
        received_exception = assertion.received_exception
        if (received_exception is not None):
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE, 'Captured exception failing the assertion:'
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE, create_break('-')
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
            yield from _produce_exception(received_exception, None)
    
    exception = assertion.exception
    if (exception is not None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE, 'Unexpected exception occurred withing the assertion:'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE, create_break('-')
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield from _produce_exception(exception, None)
    
    yield from _maybe_produce_output_report(output_report)


def _produce_function_parameters(parameters):
    """
    Renders a function's parameters.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    parameters : `list<Parameter>`
        The parameter to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    previous = None
    
    for parameter in parameters:
        if (previous is not None):
            if previous.is_positional_only() and (not parameter.is_positional_only()):
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, '    '
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '/'
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
            
            if previous.is_positional() and parameter.is_keyword_only():
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, '    '
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '*'
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, '    '
        
        # * or ** ?
        if parameter.is_args():
            prefix = '*'
        elif parameter.is_kwargs():
            prefix = '**'
        else:
            prefix = None
        
        if (prefix is not None):
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, prefix
        
        # name
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, parameter.name
        
        # default
        if parameter.has_default:
            yield from _produce_assignation()
            yield from _produce_value_representation(parameter.default)
        
        previous = parameter
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


def _produce_unsatisfied_parameters(unsatisfied_parameters):
    """
    Renders the unsatisfied parameters.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    unsatisfied_parameters : `list<Parameter>`
        The parameter to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    for parameter in unsatisfied_parameters:
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, '    '
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, parameter.name
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


def _produce_report_parameter_mismatch(report, path_parts, name, documentation_lines, call_state, output_report):
    """
    Renders parameter mismatch failure report.
    
    This functions is an iterable generator.
    
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
    
    call_state : ``None | CallState``
        Call state of the report.
    
    output_report : ``None | ReportOutput``
        Output report if any.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from produce_test_header(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        'Parameter mismatch', 
        path_parts,
        name,
        documentation_lines,
        None,
    )
    
    # Since we do not wanna render the parameters in the header, we pass the call state there as `None`
    # and then we render the case name section separately.
    if (call_state is not None):
        case_name = call_state.name
        if (case_name is not None):
            yield from produce_case_name_section(case_name)
    
    parameter_mismatch = report.parameter_mismatch
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, 'Function parameters:'
    yield from _produce_function_parameters(parameter_mismatch.parameters)
    
    yield from produce_parameters_section(
        'Given parameters:',
        parameter_mismatch.positional_parameters,
        parameter_mismatch.keyword_parameters,
    )
    
    
    unsatisfied_parameters = parameter_mismatch.unsatisfied_parameters
    if (unsatisfied_parameters is not None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, 'Unsatisfied function parameters:'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield from _produce_unsatisfied_parameters(unsatisfied_parameters)
    
    extra_positional_parameters = parameter_mismatch.extra_positional_parameters
    extra_keyword_parameters = parameter_mismatch.extra_keyword_parameters
    if (extra_positional_parameters is not None) or (extra_keyword_parameters is not None):
        yield from produce_parameters_section(
            'Extra parameters:',
            extra_positional_parameters,
            extra_keyword_parameters
        )


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


def _produce_report_raising(report, path_parts, name, documentation_lines, call_state, output_report):
    """
    Renders raising failure report.
    
    This functions is an iterable generator.
    
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
    
    call_state : ``None | CallState``
        Call state of the report.
    
    output_report : ``None | ReportOutput``
        Output report if any.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from produce_test_header(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        ('Missing exception' if report.exception_received is None else 'Unexpected exception'),
        path_parts,
        name,
        documentation_lines,
        call_state,
    )
    
    expected_exceptions = report.expected_exceptions
    if (expected_exceptions is not None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield from _produce_types_parameter_representation('expected_exceptions', expected_exceptions)
        yield from _produce_bool_non_default('accept_subtypes', report.accept_subtypes, True)
    
    
    exception_received = report.exception_received
    if (exception_received is not None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE, create_break('-')
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        yield from _produce_exception(exception_received, _ignore_invoke_test_frame)
    
    yield from _maybe_produce_output_report(output_report)


def _produce_report_returning(report, path_parts, name, documentation_lines, call_state, output_report):
    """
    Renders returning failure report.
    
    This functions is an iterable generator.
    
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
    
    call_state : ``None | CallState``
        Call state of the report.
    
    output_report : ``None | ReportOutput``
        Output report if any.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from produce_test_header(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        'Unexpected return',
        path_parts,
        name,
        documentation_lines,
        call_state,
    )
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    yield from _produce_parameter_representation('expected_return', report.expected_value)
    yield from _produce_parameter_representation('received_return', report.received_value)
    yield from _maybe_produce_output_report(output_report)


def _produce_report_unknown_failure(report, path_parts, name, documentation_lines, call_state, output_report):
    """
    Renders an unknown failure report.
    
    This functions is an iterable generator.
    
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
    
    call_state : ``None | CallState``
        Call state of the report.
    
    output_report : ``None | ReportOutput``
        Output report if any.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from produce_test_header(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_UNKNOWN,
        type(report).__name__,
        path_parts,
        name,
        documentation_lines,
        call_state,
    )
    
    yield from _maybe_produce_output_report(output_report)


FAILURE_REPORT_RENDERERS = {
    ReportFailureAsserting: _produce_report_asserting,
    ReportFailureParameterMismatch: _produce_report_parameter_mismatch,
    ReportFailureRaising: _produce_report_raising,
    ReportFailureReturning: _produce_report_returning,
}


def produce_failure_report(report, path_parts, name, documentation_lines, call_state, output_report):
    """
    Renders the given failure report.
    
    This functions is an iterable generator.
    
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
    
    call_state : ``None | CallState``
        Call state of the report.
    
    output_report : ``None | ReportOutput``
        Output report if any.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from FAILURE_REPORT_RENDERERS.get(type(report), _produce_report_unknown_failure)(
        report, path_parts, name, documentation_lines, call_state, output_report
    )
