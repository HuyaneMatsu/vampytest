__all__ = ('AssertionValueEvaluationTrue',)

from scarletio import copy_docs

from .assertion_conditional_base import AssertionConditionalBase1Value


class AssertionValueEvaluationTrue(AssertionConditionalBase1Value):
    """
    Asserts whether the value evaluates to `True`.
    
    Attributes
    ----------
    exception : `None`, `BaseException`
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
        return self.value_0
