__all__ = ('AssertionEquals',)

from . import assertion_states as CONDITION_STATES
from .assertion_conditional_base import AssertionConditionalBase


class AssertionEquals(AssertionConditionalBase):
    """
    Asserts equality.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    parameter_1 : `Any`
        First parameter to assert equality with.
    parameter_2 : `Any`
        The second parameter to assert equality with.
    """
    __slots__ = ('parameter_1', 'parameter_2',)
    
    def __new__(cls, parameter_1, parameter_2):
        """
        Asserts whether the two values are equal. Fails the test if not.
        
        Parameters
        ----------
        parameter_1 : `Any`
            First parameter to assert equality with.
        parameter_2 : `Any`
            The second parameter to assert equality with.
        """
        self = AssertionConditionalBase.__new__(cls)
        
        self.parameter_1 = parameter_1
        self.parameter_2 = parameter_2
        
        self.state = CONDITION_STATES.CREATED
        
        return self.invoke()
        
    
    def invoke_condition(self):
        """
        Invokes equality operator on the 2 parameters of the assertion.
        
        Returns
        -------
        condition_return : `Any`
            The value returned by the condition.
        """
        return self.parameter_1 == self.parameter_2
    
    
    def __repr__(self):
        """Returns the representation of the equality condition."""
        for repr_parts in self._cursed_repr_builder():
            
            repr_parts.append(', parameter_1=')
            repr_parts.append(repr(self.parameter_1))
            
            repr_parts.append(', parameter_2=')
            repr_parts.append(repr(self.parameter_2))

        return "".join(repr_parts)
