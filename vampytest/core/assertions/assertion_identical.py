__all__ = ('AssertionIdentical', 'assert_id', 'assert_is', 'assert_identical')

from .assertion_conditional_base import AssertionConditionalBase2Value

from scarletio import copy_docs


class AssertionIdentical(AssertionConditionalBase2Value):
    """
    Asserts whether two objects are identical.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    value_1 : `Any`
        First value to assert identity with.
    value_2 : `Any`
        The second value to assert identity with.
    """
    __slots__ = ('value_1', 'value_2',)
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        return self.value_1 is self.value_2
    
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'is'


assert_id = AssertionIdentical
assert_is = AssertionIdentical
assert_identical = AssertionIdentical
