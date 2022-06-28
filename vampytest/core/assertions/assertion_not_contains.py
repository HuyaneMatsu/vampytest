__all__ = ('AssertionNotContains', 'assert_not_contains', 'assert_not_in')

from .assertion_conditional_base import AssertionConditionalBase2Value

from scarletio import copy_docs

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
    value_1 : `Any`
        First value to assert contains with.
    value_2 : `Any`
        The second value to assert contains with.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        return self.value_1 not in self.value_2
    
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'not in'


assert_not_contains = AssertionNotContains
assert_not_in = AssertionNotContains
