__all__ = ()

from scarletio.utils.trace.trace import _render_exception_into

from ...runner.runner import __file__ as VAMPYTEST_RUNNER_FILE_PATH


def _ignore_invoke_test_frame(frame):
    """
    Ignores the frame where the import was called from.
    
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
    
    if file_name == VAMPYTEST_RUNNER_FILE_PATH:
        if name == '_run_generator':
            if line == '__import__(source)':
                should_show_frame = False
    
    return should_show_frame


def render_load_failure_exception_into(exception, highlight_streamer, into):
    """
    Renders load failure exception into the given list of strings.
    
    Parameters
    ----------
    exception : ``BaseException``
        The raised exception.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_exception_into(
        exception,
        _ignore_invoke_test_frame,
        highlight_streamer,
        into,
    )
