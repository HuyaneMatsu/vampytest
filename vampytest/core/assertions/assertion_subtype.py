__all__ = ('AssertionSubtype', 'assert_subtype')

from . import assertion_states as CONDITION_STATES
from .assertion_conditional_base import AssertionConditionalBase, AssertionConditionalBase2Value

from scarletio import copy_docs


class AssertionSubtype(AssertionConditionalBase2Value):
    """
    Asserts whether the first object is instance of the second one.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    value_1 : `Any`
        First value to assert subtype with.
    value_2 : `Any`
        The second value to assert subtype with.
    nullable : `bool`
        Whether `value` is accepted even if given as `None`.
    """
    __slots__ = ('nullable',)
    
    def __new__(cls, value, type_, *, reverse=False, nullable=False):
        """
        Creates a new instance assertion.
        
        Parameters
        ----------
        value : `Any`
            Object to check.
        type_ : `type_`
            Type to check.
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        nullable : `bool` = `False`, Optional (Keyword only)
            Whether `value` is accepted even if given as `None`.
        
        Raises
        ------
        TypeError
            - If `type_` is not `type` instance.
        """
        if not isinstance(type_, type):
            raise TypeError(
                f'`type_˛` parameter can be `type` instance, got {type_.__class__.__name__}; {type_!r}.'
            )
        
        self = AssertionConditionalBase.__new__(cls, reverse=reverse)
        
        self.value_1 = value
        self.value_2 = type_
        
        self.state = CONDITION_STATES.CREATED
        
        self.nullable = nullable
        
        return self.invoke()
        
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        if self.nullable:
            if self.value_1 is None:
                return True
        
        return isinstance(self.value_1, type) and issubclass(self.value_1, self.value_2)
        
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'subtype'
    
    
    @copy_docs(AssertionConditionalBase2Value._render_operation_representation_into)
    def _render_operation_representation_into(self, into):
        AssertionConditionalBase._render_operation_representation_into(self, into)
        into.append(' as "')
        if self.nullable:
            into.append('parameter_1 is None or ')
        into.append('isinstance(parameter_1, type) and issubclass(parameter_1, parameter_2)"')
        return into


assert_subtype = AssertionSubtype
