__all__ = ('TestDoneEvent',)

from .base import ResultGroupEventBase
from .constants import IDENTIFIER_TEST_DONE


class TestDoneEvent(ResultGroupEventBase):
    """
    Dispatched when a test case was executed.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    result_group : ``ResultGroup``
        The respective result group.
    """
    __slots__ = ()
    
    identifier = IDENTIFIER_TEST_DONE
