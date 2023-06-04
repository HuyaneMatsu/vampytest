__all__ = ('TestDoneEvent',)

from .base import ResultEventBase
from .constants import IDENTIFIER_TEST_DONE


class TestDoneEvent(ResultEventBase):
    """
    Dispatched when a test case was executed.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    result : ``Result``
        The respective result.
    """
    __slots__ = ()
    
    identifier = IDENTIFIER_TEST_DONE
