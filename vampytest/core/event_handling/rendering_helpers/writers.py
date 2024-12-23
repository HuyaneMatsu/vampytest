__all__ = ()

from scarletio import DEFAULT_ANSI_HIGHLIGHTER, HIGHLIGHT_TOKEN_TYPES, add_highlighted_part_into, render_exception_into

from ...file.load_failure import _ignore_module_import_frame

from .result_rendering import render_result_failing_into, render_result_informal_into


def write_load_failure(output_writer, load_failure, highlighter):
    """
    Writes load failure.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    
    load_failure : ``TestFileLoadFailure``
        Test file load failure.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    """
    message_parts = []
    message_parts = add_highlighted_part_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE, 'Exception occurred while loading:', highlighter, message_parts
    )
    message_parts.append('\n')
    message_parts = add_highlighted_part_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_LOCATION_PATH, load_failure.path, highlighter, message_parts
    )
    message_parts.append('\n\n')
    message_parts = render_exception_into(
        load_failure.exception,
        message_parts,
        filter = _ignore_module_import_frame,
        highlighter = DEFAULT_ANSI_HIGHLIGHTER,
    )
    
    output_writer.write_line(''.join(message_parts))
    output_writer.write_break_line()


def write_result_failing(output_writer, result, highlighter):
    """
    Writes a failing test.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    
    result : ``Result``
        The failing test.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    """
    message_parts = []
    message_parts = render_result_failing_into(result, highlighter, message_parts)
    output_writer.write_line(''.join(message_parts))
    output_writer.write_break_line()


def write_result_informal(output_writer, result, highlighter):
    """
    Writes the extra information attached to the test.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    
    result : ``Result``
        The informal test.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    """
    message_parts = []
    message_parts = render_result_informal_into(result, highlighter, message_parts)
    if message_parts:
        output_writer.write_line(''.join(message_parts))
        output_writer.write_break_line()
