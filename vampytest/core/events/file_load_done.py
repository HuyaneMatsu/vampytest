__all__ = ('FileLoadDoneEvent',)

from .base import FileEventBase
from .constants import IDENTIFIER_FILE_LOAD_DONE


class FileLoadDoneEvent(FileEventBase):
    """
    Dispatched when a test file's loading is done.
    
    Test files can be either be loaded with success or failure. To check it use the
    ``TestFile.is_loaded_with_success`` or the ``TestFile.is_loaded_with_success`` methods.
    
    To get details about why loading the file failed use the ``TestFile.is_loaded_with_success`` method.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    file : ``TestFile``
        The respective test file.
    """
    __slots__ = ()
    
    identifier = IDENTIFIER_FILE_LOAD_DONE
