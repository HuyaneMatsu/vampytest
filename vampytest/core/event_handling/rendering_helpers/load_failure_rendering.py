__all__ = ()

from scarletio.utils.trace.trace import _produce_exception

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


def produce_load_failure_exception(exception):
    """
    Renders load failure exception into the given list of strings.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    exception : `BaseException`
        The raised exception.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_exception(exception, _ignore_invoke_test_frame)
