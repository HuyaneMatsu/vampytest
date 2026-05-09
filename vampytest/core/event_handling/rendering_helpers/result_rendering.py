__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES

from .report_rendering import produce_failure_report, produce_output_report
from .result_rendering_common import produce_test_header


def produce_result_reversed(result):
    """
    Creates a reversed failure message for the given test handle.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    result : ``Result``
        Test result.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from produce_test_header(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        'Reversed test passed',
        result.case.path_parts,
        result.case.name,
        result.handle.get_test_documentation_lines(),
        result.handle.final_call_state,
    )


def produce_result_wrapper_conflict(result):
    """
    Renders wrapper conflict.
    
    This function is an iterable generator.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    into = produce_test_header(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        'Wrapper conflict', 
        result.case.path_parts,
        result.case.name,
        result.handle.get_test_documentation_lines(),
        None,
    )
    
    wrapper_conflict = result.wrapper_conflict
    reason = wrapper_conflict.reason
    if (reason is not None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, 'Reason: '
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_POSITIVE, reason
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, 'Between wrapper(s):'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX, '-',
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT, repr(wrapper_conflict.wrapper_0)
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    
    wrapper_1 = wrapper_conflict.wrapper_1
    if (wrapper_1 is not None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX, '-'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT, repr(wrapper_conflict.wrapper_1)
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    
    return into


def produce_result_failure_report(result):
    """
    Renders a failure report.
    
    This function is an iterable generator.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from produce_failure_report(
        result.get_failure_report(),
        result.case.path_parts,
        result.case.name,
        result.handle.get_test_documentation_lines(),
        result.handle.final_call_state,
        result.get_output_report(),
    )


def produce_result_failing(result):
    """
    Renders a failing result.
    
    This function is an iterable generator.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    if result.is_conflicted():
        producer = produce_result_wrapper_conflict
    elif result.reversed:
        producer = produce_result_reversed
    else:
        producer = produce_result_failure_report
    
    yield from producer(result)


def produce_result_informal(result):
    """
    Renders an informal result.
    
    This function is an iterable generator.
    
    Parameter
    ---------
    result : ``Result``
        The result failing with wrapper conflict.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    output_report = result.get_output_report()
    if (output_report is not None):
        yield from produce_output_report(
            output_report, 
            result.case.path_parts,
            result.case.name,
            result.handle.get_test_documentation_lines(),
            result.handle.final_call_state,
        )
