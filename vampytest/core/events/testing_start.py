__all__ = ('TestingStartEvent',)

from .base import EventBase
from .constants import IDENTIFIER_TESTING_START


class TestingStartEvent(EventBase):
    """
    Dispatched when testing is started.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    """
    __slots__ = ()
    
    identifier = IDENTIFIER_TESTING_START
