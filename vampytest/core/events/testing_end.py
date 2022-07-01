__all__ = ('TestingEndEvent',)

from .base import EventBase
from .constants import IDENTIFIER_TESTING_END


class TestingEndEvent(EventBase):
    """
    Dispatched when testing is ended.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    """
    __slots__ = ()
    
    identifier = IDENTIFIER_TESTING_END
