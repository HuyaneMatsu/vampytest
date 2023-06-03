__all__ = ('AssertionConditionalBase', 'AssertionConditionalBase1Value', 'AssertionConditionalBase2Value')

from scarletio import copy_docs, include

from .assertion_base import AssertionBase
from .assertion_states import ASSERTION_STATE_CREATED, ASSERTION_STATE_PASSED, ASSERTION_STATE_FAILED


AssertionException = include('AssertionException')


class InvokeAfterConstructor(type):
    """
    Metatype for invoking a test after calling its `__new__`.
    """
    def __call__(type_, *positional_parameters, **keyword_parameter):
        """
        Instantiates the type and invokes it.
        
        Parameters
        ----------
        type_ : `type`
            The type to Instantiate and invoke.
        *positional_parameters : `tuple<object>`
            Positional parameters to pass to the type's constructor.
        keyword_parameter : `dict<str, object>`
            Keyword parameters to pass to the type's constructor.
        
        Returns
        -------
        condition_return : `object`
            The returned value by the condition. Usually a boolean.
        
        Raises
        ------
        AssertionException
            The condition failed.
        BaseException
            An other occurred exceptions.
        """
        return type_.__new__(type_, *positional_parameters, **keyword_parameter).invoke()


class AssertionConditionalBase(AssertionBase, metaclass = InvokeAfterConstructor):
    """
    Base class for conditional assertions.
    
    Attributes
    ----------
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    reverse : `bool`
        Whether the condition should be reversed.
    state : `str`
        The condition's state.
    """
    __slots__ = ('exception', 'reverse')
    
    def __new__(cls, *, reverse = False):
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
        self.state = ASSERTION_STATE_CREATED
        return self
    
    
    @copy_docs(AssertionBase._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into = AssertionBase._build_repr_parts_into(self, into)
        
        reverse = self.reverse
        if reverse:
            into.append(', reverse = ')
            into.append(repr(reverse))
            
        
        exception = self.exception
        if (exception is not None):
            into.append(', exception = ')
            into.append(repr(exception))
        
        return into
    
    
    def invoke(self):
        """
        Invokes the assertion.
        
        Returns
        -------
        condition_return : `object`
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
            self.state = ASSERTION_STATE_FAILED
            self.exception = err
            
        else:
            if self.reverse:
                passed = not passed
            
            if passed:
                self.state = ASSERTION_STATE_PASSED
                return condition_return
            
            self.state = ASSERTION_STATE_FAILED
        
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
        result : `object`
            The condition's result.
        """
        raise NotImplementedError
    
    
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


def _render_parameters_representation_into(parameter_name, parameter_value, into):
    """
    Renders the given parameter into the given list of strings.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name.
    parameter_value : `object`
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


def _render_types_parameter_representation_into(parameter_name, types, into):
    """
    Renders the given types parameter into the given list of strings.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter's name.
    types : `set` of `type`
        The parameter's value.
    into : `list` of `str`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(parameter_name)
    into.append(' = ')
    
    type_representations = sorted(str(type.__name__) for type in types)
    length = len(type_representations)
    if length:
        index = 0
        
        while True:
            type_representation = type_representations[index]
            into.append(type_representation)
            
            index += 1
            if index == length:
                break
            
            into.append(', ')
            continue
    
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
    value_0 : `object`
        The value to call the condition on.
    """
    __slots__ = ('value_0',)

    def __new__(cls, value_0, *, reverse = False):
        """
        Asserts whether the two values are equal. Fails the test if not.
        
        Parameters
        ----------
        value_0 : `object`
            First value to assert equality with.
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        """
        self = AssertionConditionalBase.__new__(cls, reverse = reverse)
        self.value_0 = value_0
        return self
    
    
    @copy_docs(AssertionConditionalBase._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into = AssertionConditionalBase._build_repr_parts_into(self, into)
        
        into.append(', value_0 = ')
        into.append(repr(self.value_0))
        
        return into
    
    
    @copy_docs(AssertionConditionalBase.render_failure_message_parts_into)
    def render_failure_message_parts_into(self, failure_message_parts):
        AssertionConditionalBase.render_failure_message_parts_into(self, failure_message_parts)
        _render_parameters_representation_into('parameter', self.value_0, failure_message_parts)
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
    value_0 : `object`
        The value to call the condition on.
    value_1 : `object`
        The value to call the condition with.
    """
    __slots__ = ('value_1',)
    
    def __new__(cls, value_0, value_1, *, reverse = False):
        """
        Asserts whether the two values are equal. Fails the test if not.
        
        Parameters
        ----------
        value_0 : `object`
            First value to assert equality with.
        value_1 : `object`
            The second value to assert equality with.
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        """
        self = AssertionConditionalBase1Value.__new__(cls, value_0, reverse = reverse)
        self.value_1 = value_1
        return self
    
    
    @copy_docs(AssertionConditionalBase1Value._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into = AssertionConditionalBase1Value._build_repr_parts_into(self, into)
        
        into.append(', value_1 = ')
        into.append(repr(self.value_1))
        
        return into
    
    
    @copy_docs(AssertionConditionalBase1Value._render_operation_representation_into)
    def _render_operation_representation_into(self, into):
        AssertionConditionalBase._render_operation_representation_into(self, into)
        into.append(' as "parameter_0 ')
        into.append(self._get_operation_representation())
        into.append(' parameter_1"')
        return into
    
    
    @copy_docs(AssertionConditionalBase1Value.render_failure_message_parts_into)
    def render_failure_message_parts_into(self, failure_message_parts):
        AssertionConditionalBase.render_failure_message_parts_into(self, failure_message_parts)
        _render_parameters_representation_into('parameter_0', self.value_0, failure_message_parts)
        _render_parameters_representation_into('parameter_1', self.value_1, failure_message_parts)
        return failure_message_parts
