__all__ = ()

from ...result import (
    ReportFailureAsserting, ReportFailureParameterMismatch, ReportFailureRaising, ReportFailureReturning
)

from ..colors import COLOR_FAIL, COLOR_PATH
from ..text_styling import style_text_into

from .result_rendering import (
    render_report_asserting_into, render_report_output_into, render_report_parameter_mismatch_into,
    render_report_raising_into, render_report_returning_into, render_report_reversed_into, render_wrapper_conflict_into
)


def write_load_failure(output_writer, load_failure):
    """
    Writes load failure.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    load_failure : ``TestFileLoadFailure``
        Test file load failure.
    """
    message_parts = []
    message_parts = style_text_into(message_parts, 'Exception occurred while loading:\n', COLOR_FAIL)
    message_parts = style_text_into(message_parts, load_failure.path, COLOR_PATH)
    message_parts.append('\n\n')
    message_parts = style_text_into(message_parts, load_failure.exception_message, COLOR_FAIL)
    
    output_writer.write_line(''.join(message_parts))
    output_writer.write_break_line()


def write_result_failing(output_writer, result):
    """
    Writes a failing test.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    result : ``Result``
        The failing test.
    """
    message_parts = []
    
    if result.is_conflicted():
        message_parts = render_wrapper_conflict_into(message_parts, result)
    
    elif result.reversed:
        message_parts = render_report_reversed_into(message_parts, result)
    
    else:
        failure_report = result.get_failure_report()
        if isinstance(failure_report, ReportFailureAsserting):
            message_parts = render_report_asserting_into(message_parts, result, failure_report)
        
        elif isinstance(failure_report, ReportFailureRaising):
            message_parts = render_report_raising_into(message_parts, result, failure_report)
        
        elif isinstance(failure_report, ReportFailureReturning):
            message_parts = render_report_returning_into(message_parts, result, failure_report)
        
        elif isinstance(failure_report, ReportFailureParameterMismatch):
            message_parts = render_report_parameter_mismatch_into(message_parts, result, failure_report)
            
        else:
            # No other case.
            return
        
    output_writer.write_line(''.join(message_parts))
    output_writer.write_break_line()


def write_result_informal(output_writer, result):
    """
    Writes the extra information attached to the test.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    result : ``Result``
        The informal test.
    """
    output_report = result.get_output_report()
    if output_report is None:
        return
    
    message_parts = []
    render_report_output_into(message_parts, result, output_report)
    output_writer.write_line(''.join(message_parts))
    output_writer.write_break_line()
    
