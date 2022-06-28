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
    reverse : `bool`
        Whether the condition should be reversed.
    value_1 : `Any`
        First value to assert.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase1Value.invoke_condition)
    def invoke_condition(self):
        return self.value_1
    
    
    @copy_docs(AssertionConditionalBase1Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'bool(...)'

    @copy_docs(AssertionConditionalBase1Value._render_operation_representation_into)
    def _render_operation_representation_into(self, into):
        AssertionConditionalBase1Value._render_operation_representation_into(self, into)
        into.append(' as "bool(parameter)"')
        return into


assert_ = AssertionValueEvaluationTrue
assert_true = AssertionValueEvaluationTrue
