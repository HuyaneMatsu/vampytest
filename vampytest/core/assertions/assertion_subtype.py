__all__ = ('AssertionSubtype',)

from scarletio import copy_docs

from ..helpers.un_nesting import un_nest_types

from .assertion_conditional_base import AssertionConditionalBase2Value


class AssertionSubtype(AssertionConditionalBase2Value):
    """
    Asserts whether the first object is instance of the second one.
    
    Attributes
    ----------
    exception : `None | BaseException`
        Exception raised by the condition if any.
    
    nullable : `bool`
        Whether `value` is accepted even if given as `None`.
    
    reverse : `bool`
        Whether the condition should be reversed.
    
    state : `int`
        The condition's state.
    
    value_0 : `object`
        First value to assert subtype with.
    
    value_1 : `object`
        The second value to assert subtype with.
    """
    __slots__ = ('nullable',)
    
    def __new__(cls, value, accepted_type, *accepted_types, reverse = False, nullable = False):
        """
        Creates a new instance assertion.
        
        Parameters
        ----------
        value : `object`
            Object to check.
        
        accepted_type : `type`
            Type to check.
        
        *accepted_types : `tuple<type>`
            Additional types to check.
        
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        
        nullable : `bool` = `False`, Optional (Keyword only)
            Whether `value` is accepted even if given as `None`.
        
        Raises
        ------
        TypeError
            - If `accepted_type` is not `type` instance.
        ValueError
            - No types given.
        """
        accepted_types = un_nest_types((accepted_type, *accepted_types))
        if not accepted_types:
            raise ValueError(
                'At least 1 type is required.'
            )
        
        self = AssertionConditionalBase2Value.__new__(cls, value, accepted_types, reverse = reverse)
        self.nullable = nullable
        return self
    
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self): 
        value = self.value_0
        accepted_types = self.value_1
        
        if self.nullable and value is None:
            return True
        
        return isinstance(value, type) and any(issubclass(value, accepted_type) for accepted_type in accepted_types)
    
    
    @copy_docs(AssertionConditionalBase2Value._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into = AssertionConditionalBase2Value._build_repr_parts_into(self, into)
        
        nullable = self.nullable
        if nullable:
            into.append(', nullable = ')
            into.append(repr(nullable))
        
        return into
