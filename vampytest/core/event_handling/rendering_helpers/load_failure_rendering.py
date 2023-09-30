__all__ = ()

from scarletio import DEFAULT_ANSI_HIGHLIGHTER, render_exception_into

from ...runner.runner import __file__ as VAMPYTEST_RUNNER_FILE_PATH


def ignore_invoke_test_frame(file_name, name, line_number, line):
    """
    Ignores the frame where the import was called from.
    
    Parameters
    ----------
    file_name : `str`
        The frame's respective file's name.
    name : `str`
        The frame's respective function's name.
    line_number : `int`
        The line's index where the exception occurred.
    line : `str`
        The frame's respective stripped line.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    if file_name == VAMPYTEST_RUNNER_FILE_PATH:
        if name == '_run_generator':
            if line == '__import__(source)':
                should_show_frame = False
    
    return should_show_frame


def render_load_failure_exception(exception):
    """
    Renders load failure exception
    
    Parameters
    ----------
    exception : ``BaseException``
        The raised exception.
    
    Returns
    -------
    rendered : `str`
    """
    return ''.join(
        render_exception_into(
            exception,
            [],
            filter = ignore_invoke_test_frame,
            highlighter = DEFAULT_ANSI_HIGHLIGHTER
        )
    )
