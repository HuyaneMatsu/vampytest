__all__ = ('AssertionContains',)

from . import assertion_states as CONDITION_STATES
from .assertion_conditional_base import AssertionConditionalBase2Value


class AssertionContains(AssertionConditionalBase2Value):
    """
    Asserts equality.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    value_1 : `Any`
        First value to assert contains with.
    value_2 : `Any`
        The second value to assert contains with.
    """
    __slots__ = ()
    
    def invoke_condition(self):
        """
        Invokes equality operator on the 2 values of the assertion.
        
        Returns
        -------
        condition_return : `Any`
            The value returned by the condition.
        """
        return self.value_1 in self.value_2
