__all__ = ('AssertionNotIdentical', 'assert_is_not', 'assert_not_id', 'assert_not_identical', 'assert_not_is')

from .assertion_conditional_base import AssertionConditionalBase2Value

from scarletio import copy_docs


class AssertionNotIdentical(AssertionConditionalBase2Value):
    """
    Asserts whether two objects are not identical.
    
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
        return self.value_1 is not self.value_2
    
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'is not'


assert_not_id = AssertionNotIdentical
assert_is_not = AssertionNotIdentical
assert_not_identical = AssertionNotIdentical
assert_not_is = AssertionNotIdentical
