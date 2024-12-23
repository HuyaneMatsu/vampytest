__all__ = ('AssertionValueEvaluationFalse',)

from scarletio import copy_docs

from .assertion_conditional_base import AssertionConditionalBase1Value


class AssertionValueEvaluationFalse(AssertionConditionalBase1Value):
    """
    Asserts whether the value evaluates to `False`.
    
    Attributes
    ----------
    exception : `None | BaseException`
        Exception raised by the condition if any.
    
    reverse : `bool`
        Whether the condition should be reversed.
    
    state : `int`
        The condition's state.
    
    value_0 : `object`
        First value to assert.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase1Value.invoke_condition)
    def invoke_condition(self):
        return not self.value_0
