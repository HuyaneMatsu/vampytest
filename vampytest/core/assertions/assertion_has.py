__all__ = ('AssertionHas',)

from scarletio import copy_docs

from .assertion_conditional_base import AssertionConditionalBase2Value


class AssertionHas(AssertionConditionalBase2Value):
    """
    Asserts whether the first value has the second in it.
    
    Attributes
    ----------
    exception : `None | BaseException`
        Exception raised by the condition if any.
    
    reverse : `bool`
        Whether the condition should be reversed.
    
    state : `int`
        The condition's state.
    
    value_0 : `object`
        First value to assert contains with.
    
    value_1 : `object`
        The second value to assert contains with.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        return self.value_1 in self.value_0
