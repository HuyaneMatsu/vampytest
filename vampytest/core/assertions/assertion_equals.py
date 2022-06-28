__all__ = ('AssertionEquals', 'assert_eq', 'assert_equals')

from .assertion_conditional_base import AssertionConditionalBase2Value

from scarletio import copy_docs


class AssertionEquals(AssertionConditionalBase2Value):
    """
    Asserts equality.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    value_1 : `Any`
        First value to assert equality with.
    value_2 : `Any`
        The second value to assert equality with.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        return self.value_1 == self.value_2
    
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return '=='


assert_eq = AssertionEquals
assert_equals = AssertionEquals
