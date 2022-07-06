__all__ = ('AssertionConditionalBase', 'AssertionConditionalBase1Value', 'AssertionConditionalBase2Value')

from scarletio import copy_docs, include

from . import assertion_states as CONDITION_STATES
from .assertion_base import AssertionBase


AssertionException = include('AssertionException')


class AssertionConditionalBase(AssertionBase):
    """
    Base class for conditional assertions.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    """
    __slots__ = ('exception', 'reverse')
    
    def __new__(cls, *, reverse=False):
        """
        Creates an new conditional assertion instance.
        
        Parameters
        ----------
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        """
        self = AssertionBase.__new__(cls)
        self.exception = None
        self.reverse = reverse
        return self
    
    
    @copy_docs(AssertionBase._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in AssertionBase._cursed_repr_builder(self):
            yield repr_parts
            
            reverse = self.reverse
            if reverse:
                repr_parts.append(', reverse=')
                repr_parts.append(repr(reverse))
                
            
            exception = self.exception
            if (exception is not None):
                repr_parts.append(', exception=')
                repr_parts.append(repr(exception))
    
    
    def invoke(self):
        """
        Invokes the assertion.
        
        Returns
        -------
        condition_return : `Any`
            The value returned by the condition.
        
        Raises
        ------
        AssertionException
            The condition failed.
        """
        try:
            condition_return = self.invoke_condition()
            
            if condition_return:
                passed = True
            else:
                passed = False
        
        except BaseException as err:
            self.state = CONDITION_STATES.FAILED
            self.exception = err
            
        else:
            if self.reverse:
                passed = not passed
            
            if passed:
                self.state = CONDITION_STATES.PASSED
                return condition_return
            
            self.state = CONDITION_STATES.FAILED
        
        try:
            raise AssertionException(self)
        finally:
            # Remove self reference, so garbage collection wont fail
            self = None
    
    
    def invoke_condition(self):
        """
        Invokes the condition.
        
        Returns
        -------
        result : `Any`
            The condition's result.
        """
        raise NotImplemented
    
    
    def _get_operation_representation(self):
        """
        Gets the assertion's operation's representation.
        
        Returns
        -------
        operation_representation : `str`
        """
        return ''
    
    
    def _render_operation_representation_into(self, into):
        """
        Adds the operation representation to the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            A list to extend with the rendered strings.
        
        Returns
        -------
        into : `list` of `str`
        """
        into.append('Operation: "')
        into.append(self._get_operation_representation())
        into.append('"')
        
        if self.reverse:
            into.append(' (reversed)')
        
        return into
    
    
    @copy_docs(AssertionBase.render_failure_message_parts_into)
    def render_failure_message_parts_into(self, failure_message_parts):
        self._render_operation_representation_into(failure_message_parts)
        failure_message_parts.append('\n')
        return failure_message_parts


def _add_parameters_representation_into(parameter_name, parameter_value, into):
    """
    Renders the given parameter into the given list of strings.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name.
    parameter_value : `Any`
        The parameter's value.
    into : `list` of `str`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(parameter_name)
    into.append(' = ')
    into.append(repr(parameter_value))
    into.append('\n')
    
    return into


class AssertionConditionalBase1Value(AssertionConditionalBase):
    """
    Base class for executing a one value assertion.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    value_1 : `Any`
        The value to call the condition on.
    """
    __slots__ = ('value_1',)

    def __new__(cls, value_1, *, reverse=False):
        """
        Asserts whether the two values are equal. Fails the test if not.
        
        Parameters
        ----------
        value_1 : `Any`
            First value to assert equality with.
        value_2 : `Any`
            The second value to assert equality with.
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        """
        self = AssertionConditionalBase.__new__(cls, reverse=reverse)
        
        self.value_1 = value_1
        
        self.state = CONDITION_STATES.CREATED
        
        return self.invoke()
    
    
    @copy_docs(AssertionConditionalBase._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in AssertionConditionalBase._cursed_repr_builder(self):
            
            repr_parts.append(', value_1=')
            repr_parts.append(repr(self.value_1))
            
            yield repr_parts
    
    
    @copy_docs(AssertionConditionalBase.render_failure_message_parts_into)
    def render_failure_message_parts_into(self, failure_message_parts):
        AssertionConditionalBase.render_failure_message_parts_into(self, failure_message_parts)
        _add_parameters_representation_into('parameter', self.value_1, failure_message_parts)
        return failure_message_parts


class AssertionConditionalBase2Value(AssertionConditionalBase1Value):
    """
    Base class for executing a two value assertion.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    value_1 : `Any`
        The value to call the condition on.
    value_2 : `Any`
        The value to call the condition with.
    """
    __slots__ = ('value_2',)
    
    def __new__(cls, value_1, value_2, *, reverse=False):
        """
        Asserts whether the two values are equal. Fails the test if not.
        
        Parameters
        ----------
        value_1 : `Any`
            First value to assert equality with.
        value_2 : `Any`
            The second value to assert equality with.
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        """
        self = AssertionConditionalBase.__new__(cls, reverse=reverse)
        
        self.value_1 = value_1
        self.value_2 = value_2
        
        self.state = CONDITION_STATES.CREATED
        
        return self.invoke()
    
    
    @copy_docs(AssertionConditionalBase1Value._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in AssertionConditionalBase1Value._cursed_repr_builder(self):
            
            repr_parts.append(', value_2=')
            repr_parts.append(repr(self.value_2))
            
            yield repr_parts
    
    
    @copy_docs(AssertionConditionalBase._render_operation_representation_into)
    def _render_operation_representation_into(self, into):
        AssertionConditionalBase._render_operation_representation_into(self, into)
        into.append(' as "parameter_1 ')
        into.append(self._get_operation_representation())
        into.append(' parameter_2"')
        return into
    
    
    @copy_docs(AssertionConditionalBase.render_failure_message_parts_into)
    def render_failure_message_parts_into(self, failure_message_parts):
        AssertionConditionalBase.render_failure_message_parts_into(self, failure_message_parts)
        _add_parameters_representation_into('parameter_1', self.value_1, failure_message_parts)
        _add_parameters_representation_into('parameter_2', self.value_2, failure_message_parts)
        return failure_message_parts
