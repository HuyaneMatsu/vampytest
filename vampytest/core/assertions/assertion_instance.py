__all__ = ('AssertionInstance', 'assert_instance')

from . import assertion_states as CONDITION_STATES
from .assertion_conditional_base import AssertionConditionalBase, AssertionConditionalBase2Value

from scarletio import copy_docs


class AssertionInstance(AssertionConditionalBase2Value):
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
        First value to assert instance with.
    value_2 : `Any`
        The second value to assert instance with.
    """
    __slots__ = ('accept_subtypes',)
    
    def __new__(cls, value, type_, *, reverse=False, accept_subtypes=True):
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
        accept_subtypes : `bool` = `True`, optional (Keyword only)
            Whether subclasses are accepted as well.
        
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
        self.accept_subtypes = accept_subtypes
        
        return self.invoke()
    
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        if self.accept_subtypes:
            return isinstance(self.value_1, self.value_2)
        
        return type(self.value_1) is self.value_2
        
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'instance'
    
    
    @copy_docs(AssertionConditionalBase2Value._render_operation_representation_into)
    def _render_operation_representation_into(self, into):
        AssertionConditionalBase._render_operation_representation_into(self, into)
        
        if self.accept_subtypes:
            into.append(' as "isinstance(parameter_1, parameter_2)"')
        else:
            into.append(' as "type(parameter_1) is parameter_2"')
        return into
    
    
    @copy_docs(AssertionConditionalBase2Value._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in AssertionConditionalBase2Value._cursed_repr_builder(self):
            
            accept_subtypes = self.accept_subtypes
            if not accept_subtypes:
                repr_parts.append(', accept_subtypes=')
                repr_parts.append(repr(accept_subtypes))
            
            yield repr_parts


assert_instance = AssertionInstance
