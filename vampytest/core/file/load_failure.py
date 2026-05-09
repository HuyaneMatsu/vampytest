__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .test_file import __file__ as VAMPYTEST_TEST_FILE_PATH


def _ignore_module_import_frame(frame):
    """
    Ignores the frame, where the test file was imported.
    
    Parameters
    ----------
    frame : ``frameProxyBase``
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
    
    if file_name == VAMPYTEST_TEST_FILE_PATH:
        if name == '_try_load_module':
            if line == '__import__(import_route)':
                should_show_frame = False
    
    return should_show_frame


class TestFileLoadFailure(RichAttributeErrorBaseType):
    """
    Represents an occurred failure meanwhile loading a test file.
    
    Attributes
    ----------
    exception : `BaseException`
        The exception.
    
    path : `str`
        The files path which failed to load.
    """
    __slots__ = ('path', 'exception')
    
    def __new__(cls, test_file, exception):
        """
        Parameters
        ----------
        test_file : ``TestFile``
            The test file which failed to load.
        exception : `BaseException`
            The occurred exception.
        """
        self = object.__new__(cls)
        self.exception = exception
        self.path = test_file.path
        return self
    
    
    def __repr__(self):
        """Returns the test loading failure's representation."""
        return f'<{type(self).__name__} of {self.path!r}>'
