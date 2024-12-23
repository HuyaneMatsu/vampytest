__all__ = ()

from scarletio import render_exception_into

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


def render_load_failure_exception(exception, highlighter):
    """
    Renders load failure exception
    
    Parameters
    ----------
    exception : ``BaseException``
        The raised exception.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    rendered : `str`
    """
    return ''.join(
        render_exception_into(
            exception,
            [],
            filter = _ignore_invoke_test_frame,
            highlighter = highlighter,
        )
    )
