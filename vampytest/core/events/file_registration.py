__all__ = ('FileRegistrationEvent',)

from .base import FileEventBase
from .constants import IDENTIFIER_FILE_REGISTRATION


class FileRegistrationEvent(FileEventBase):
    """
    Dispatched when a test file is registered.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    file : ``TestFile``
        The respective test file.
    """
    __slots__ = ()
    
    identifier = IDENTIFIER_FILE_REGISTRATION
