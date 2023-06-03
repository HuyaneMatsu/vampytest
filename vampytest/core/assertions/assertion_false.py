__all__ = ('AssertionValueEvaluationFalse',)

from scarletio import copy_docs

from .assertion_conditional_base import AssertionConditionalBase1Value


class AssertionValueEvaluationFalse(AssertionConditionalBase1Value):
    """
    Asserts whether the value evaluates to `False`.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    value_0 : `object`
        First value to assert.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase1Value.invoke_condition)
    def invoke_condition(self):
        return not self.value_0
    
    
    @copy_docs(AssertionConditionalBase1Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'not bool(...)'
    
    
    @copy_docs(AssertionConditionalBase1Value._render_operation_representation_into)
    def _render_operation_representation_into(self, into):
        AssertionConditionalBase1Value._render_operation_representation_into(self, into)
        into.append(' as "not bool(parameter)"')
        return into
