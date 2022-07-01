__all__ = ('FileRegistrationDoneEvent',)

from .base import EventBase
from .constants import IDENTIFIER_FILE_REGISTRATION_DONE


class FileRegistrationDoneEvent(EventBase):
    """
    Dispatched when all test files were registered.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    """
    __slots__ = ()
    
    identifier = IDENTIFIER_FILE_REGISTRATION_DONE
