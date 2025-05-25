__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES
from scarletio.utils.trace.trace import _produce_exception

from ...file.load_failure import _ignore_module_import_frame

from .result_rendering import produce_result_failing, produce_result_informal


def write_load_failure(output_writer, load_failure, highlight_streamer):
    """
    Writes load failure.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    
    load_failure : ``TestFileLoadFailure``
        Test file load failure.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    """
    message_parts = []
    message_parts.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
        'Exception occurred while loading:',
    )))
    message_parts.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    message_parts.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_LOCATION_PATH,
        load_failure.path,
    )))
    
    for _ in range(2):
        message_parts.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
    
    for item in _produce_exception(load_failure.exception, _ignore_module_import_frame):
        message_parts.extend(highlight_streamer.asend(item))
    
    output_writer.write_line(''.join(message_parts))
    output_writer.write_break_line()


def write_result_failing(output_writer, result, highlight_streamer):
    """
    Writes a failing test.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    
    result : ``Result``
        The failing test.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    """
    message_parts = []
    for item in produce_result_failing(result):
        message_parts.extend(highlight_streamer.asend(item))
        
    output_writer.write_line(''.join(message_parts))
    output_writer.write_break_line()


def write_result_informal(output_writer, result, highlight_streamer):
    """
    Writes the extra information attached to the test.
    
    Parameters
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    
    result : ``Result``
        The informal test.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    """
    message_parts = []
    for item in produce_result_informal(result):
        message_parts.extend(highlight_streamer.asend(item))
    
    if message_parts:
        output_writer.write_line(''.join(message_parts))
        output_writer.write_break_line()
