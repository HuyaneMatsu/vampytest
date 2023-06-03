__all__ = ('AssertionNotContains',)

from scarletio import copy_docs

from .assertion_conditional_base import AssertionConditionalBase2Value


class AssertionNotContains(AssertionConditionalBase2Value):
    """
    Asserts whether the second value not contains the first one.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    value_0 : `object`
        First value to assert contains with.
    value_1 : `object`
        The second value to assert contains with.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        return self.value_0 not in self.value_1
    
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'not in'
