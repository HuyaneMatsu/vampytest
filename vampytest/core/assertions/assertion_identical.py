__all__ = ('AssertionIdentical',)

from scarletio import copy_docs

from .assertion_conditional_base import AssertionConditionalBase2Value


class AssertionIdentical(AssertionConditionalBase2Value):
    """
    Asserts whether two objects are identical.
    
    Attributes
    ----------
    exception : `None | BaseException`
        Exception raised by the condition if any.
    
    reverse : `bool`
        Whether the condition should be reversed.
    
    state : `int`
        The condition's state.
    
    value_0 : `object`
        First value to assert identity with.
    
    value_1 : `object`
        The second value to assert identity with.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        return self.value_0 is self.value_1
