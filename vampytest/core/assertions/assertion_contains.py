__all__ = ('AssertionContains', 'assert_contains', 'assert_in',)

from .assertion_conditional_base import AssertionConditionalBase2Value

from scarletio import copy_docs


class AssertionContains(AssertionConditionalBase2Value):
    """
    Asserts whether the first value contains the second.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    value_1 : `Any`
        First value to assert contains with.
    value_2 : `Any`
        The second value to assert contains with.
    """
    __slots__ = ()
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        return self.value_1 in self.value_2

assert_contains = AssertionContains
assert_in = AssertionContains
