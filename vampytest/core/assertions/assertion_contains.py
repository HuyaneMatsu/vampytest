__all__ = ('AssertionContains',)

from . import assertion_states as CONDITION_STATES
from .assertion_conditional_base import AssertionConditionalBase


class AssertionContains(AssertionConditionalBase):
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
    __slots__ = ('value_1', 'value_2',)
    
    def __new__(cls, value_1, value_2):
        """
        Asserts whether the the first value contains the second one.
        
        Parameters
        ----------
        value_1 : `Any`
            First value to assert equality with.
        value_2 : `Any`
            The second value to assert equality with.
        """
        self = AssertionConditionalBase.__new__(cls)
        
        self.value_1 = value_1
        self.value_2 = value_2
        
        self.state = CONDITION_STATES.CREATED
        
        return self.invoke()
        
    
    def invoke_condition(self):
        """
        Invokes equality operator on the 2 values of the assertion.
        
        Returns
        -------
        condition_return : `Any`
            The value returned by the condition.
        """
        return self.value_1 in self.value_2
    
    
    def __repr__(self):
        """Returns the representation of the equality condition."""
        for repr_parts in self._cursed_repr_builder():
            
            repr_parts.append(', value_1=')
            repr_parts.append(repr(self.value_1))
            
            repr_parts.append(', value_2=')
            repr_parts.append(repr(self.value_2))

        return "".join(repr_parts)
