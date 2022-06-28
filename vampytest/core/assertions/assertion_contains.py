__all__ = ('AssertionContains', 'assert_contains', 'assert_in',)

from .assertion_conditional_base import AssertionConditionalBase2Value

from scarletio import copy_docs


class AssertionContains(AssertionConditionalBase2Value):
    """
    Asserts whether the second value contains the first.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    value_1 : `Any`
        First value to assert contains with.
    value_2 : `Any`
        The second value to assert contains with.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        return self.value_1 in self.value_2
    
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'in'


assert_contains = AssertionContains
assert_in = AssertionContains
