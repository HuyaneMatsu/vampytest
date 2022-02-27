__all__ = ('AssertionIdentity',)

from . import assertion_states as CONDITION_STATES
from .assertion_conditional_base import AssertionConditionalBase

from scarletio import copy_docs

class AssertionIdentity(AssertionConditionalBase):
    """
    Asserts identity.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    value_1 : `Any`
        First value to assert identity with.
    value_2 : `Any`
        The second value to assert identity with.
    """
    __slots__ = ('value_1', 'value_2',)
    
    def __new__(cls, value_1, value_2):
        """
        Asserts whether the two values are the same. Fails the test if not.
        
        Parameters
        ----------
        value_1 : `Any`
            First value to assert identity with.
        value_2 : `Any`
            The second value to assert identity with.
        """
        self = AssertionConditionalBase.__new__(cls)
        
        self.value_1 = value_1
        self.value_2 = value_2
        
        self.state = CONDITION_STATES.CREATED
        
        return self.invoke()
    
    
    @copy_docs(AssertionConditionalBase.invoke_condition)
    def invoke_condition(self):
        return self.value_1 is self.value_2
    
    
    @copy_docs(AssertionConditionalBase.__repr__)
    def __repr__(self):
        for repr_parts in self._cursed_repr_builder():
            
            repr_parts.append(', value_1=')
            repr_parts.append(repr(self.value_1))
            
            repr_parts.append(', value_2=')
            repr_parts.append(repr(self.value_2))

        return "".join(repr_parts)
