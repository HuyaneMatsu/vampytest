__all__ = ('AssertionValueEvaluationTrue', 'assert_', 'assert_true',)

from .assertion_conditional_base import AssertionConditionalBase1Value

from scarletio import copy_docs


class AssertionValueEvaluationTrue(AssertionConditionalBase1Value):
    """
    Asserts whether the value evaluates to `True`.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    value_1 : `Any`
        First value to assert.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase1Value.invoke_condition)
    def invoke_condition(self):
        return self.value_1

assert_ = AssertionValueEvaluationTrue
assert_true = AssertionValueEvaluationTrue
