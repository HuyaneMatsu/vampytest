__all__ = ('FileTestingDoneEvent',)

from .base import FileEventBase
from .constants import IDENTIFIER_FILE_TESTING_DONE


class FileTestingDoneEvent(FileEventBase):
    """
    Dispatched when a test file's all tests ran.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    file : ``TestFile``
        The respective test file.
    """
    __slots__ = ()
    
    identifier = IDENTIFIER_FILE_TESTING_DONE
