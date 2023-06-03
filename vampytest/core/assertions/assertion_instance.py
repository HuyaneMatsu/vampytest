__all__ = ('AssertionInstance',)

from scarletio import copy_docs

from ..helpers.un_nesting import un_nest_types

from .assertion_conditional_base import (
    AssertionConditionalBase, AssertionConditionalBase2Value, _render_parameters_representation_into,
    _render_types_parameter_representation_into
)


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
    value_0 : `object`
        First value to assert instance with.
    value_1 : `set` of `type<type>`
        The second value to assert instance with.
    accept_subtypes : `bool`
        Whether instances of subtypes should be accepted.
    nullable : `bool`
        Whether `value` is accepted even if given as `None`.
    """
    __slots__ = ('accept_subtypes', 'nullable')
    
    def __new__(cls, value, accepted_type, *accepted_types, accept_subtypes = True, reverse = False, nullable = False):
        """
        Creates a new instance assertion.
        
        Parameters
        ----------
        value : `object`
            Object to check.
        accepted_type : `type<type>`
            The type to check.
        *accepted_types : `tuple<type<type>, ...>`
            Additional accepted types.
        accept_subtypes : `bool` = `True`, Optional (Keyword only)
            Whether instances of subtypes should be accepted.
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        nullable : `bool` = `False`, Optional (Keyword only)
            Whether `value` is accepted even if given as `None`.
        
        Raises
        ------
        TypeError
            - If a type`` is not `type` instance.
        ValueError
            - No types given.
        """
        accepted_types = un_nest_types((accepted_type, *accepted_types))
        if not accepted_types:
            raise ValueError(
                'At least 1 type is required.'
            )
        
        self = AssertionConditionalBase2Value.__new__(cls, value, accepted_types, reverse = reverse)
        self.accept_subtypes = accept_subtypes
        self.nullable = nullable
        return self
    
    
    @copy_docs(AssertionConditionalBase2Value.invoke_condition)
    def invoke_condition(self):
        value = self.value_0
        accepted_types = self.value_1
        
        if self.nullable:
            if value is None:
                return True
        
        value_type = type(value)
        
        if self.accept_subtypes:
            return any(issubclass(value_type, accepted_type) for accepted_type in accepted_types)
        
        return any((value_type is accepted_type) for accepted_type in accepted_types)
    
    
    @copy_docs(AssertionConditionalBase2Value._get_operation_representation)
    def _get_operation_representation(self):
        return 'instance'
    
    
    @copy_docs(AssertionConditionalBase2Value._render_operation_representation_into)
    def _render_operation_representation_into(self, into):
        AssertionConditionalBase._render_operation_representation_into(self, into)
        
        into.append(' as "')
        
        if self.nullable:
            into.append('value is None or ')
        
        if self.accept_subtypes:
            instance_check_part = 'isinstance(value, expected_types)'
        else:
            instance_check_part = 'type(value) is expected_types'
        into.append(instance_check_part)
        into.append('"')
        
        return into
    
    
    @copy_docs(AssertionConditionalBase2Value._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into = AssertionConditionalBase2Value._build_repr_parts_into(self, into)
        
        accept_subtypes = self.accept_subtypes
        if not accept_subtypes:
            into.append(', accept_subtypes = ')
            into.append(repr(accept_subtypes))
        
        nullable = self.nullable
        if nullable:
            into.append(', nullable = ')
            into.append(repr(nullable))
        
        return into
    
    
    @copy_docs(AssertionConditionalBase2Value.render_failure_message_parts_into)
    def render_failure_message_parts_into(self, failure_message_parts):
        AssertionConditionalBase.render_failure_message_parts_into(self, failure_message_parts)
        _render_parameters_representation_into('value', self.value_0, failure_message_parts)
        _render_types_parameter_representation_into('expected_types', self.value_1, failure_message_parts)
        return failure_message_parts
