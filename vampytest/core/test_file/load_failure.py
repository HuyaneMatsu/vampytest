__all__ = ()

import reprlib

from .test_file import __file__ as VAMPYTEST_TEST_FILE_PATH

from scarletio import RichAttributeErrorBaseType, render_exception_into


def _ignore_module_import_frame(file_name, name, line_number, line):
    """
    Ignores the frame, where the test file was imported.
    
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
    exception_message : `str`
        Exception message with traceback.
    path : `str`
        The files path which failed to load.
    """
    __slots__ = ('path', 'exception_message')
    
    def __new__(cls, test_file, exception):
        """
        Parameters
        ----------
        test_file : ``TestFile``
            The test file which failed to load.
        exception : `BaseException`
            The occurred exception.
        """
        exception_message_parts = []
        render_exception_into(exception, exception_message_parts, filter=_ignore_module_import_frame)
        exception_message = ''.join(exception_message_parts)
        
        self = object.__new__(cls)
        self.exception_message = exception_message
        self.path = test_file.path
        return self
    
    
    def __repr__(self):
        """Returns the test loading failure's representation."""
        return f'<{self.__class__.__name__} of {reprlib.repr(self.path)}>'
