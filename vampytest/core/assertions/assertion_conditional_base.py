__all__ = ('AssertionConditionalBase', 'AssertionConditionalBase1Value', 'AssertionConditionalBase2Value')

from . import assertion_states as CONDITION_STATES
from .assertion_base import AssertionBase
from .exceptions import AssertionException

from scarletio import copy_docs

class AssertionConditionalBase(AssertionBase):
    """
    Base class for conditional assertions.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    """
    __slots__ = ('exception', )
    
    def __new__(cls):
        """
        Creates an new conditional assertion instance.
        """
        self = AssertionBase.__new__(cls)
        self.exception = None
        return self
    
    
    @copy_docs(AssertionBase._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in AssertionBase._cursed_repr_builder(self):
            yield repr_parts
            
            exception = self.exception
            if (exception is not None):
                repr_parts.append(', exception=')
                repr_parts.append(repr(self.exception))
    
    
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


class AssertionConditionalBase1Value(AssertionConditionalBase):
    """
    Base class for executing a one value assertion.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    value_1 : `Any`
        The value to call the condition on.
    """
    __slots__ = ('value_1',)

    def __new__(cls, value_1):
        """
        Asserts whether the two values are equal. Fails the test if not.
        
        Parameters
        ----------
        value_1 : `Any`
            First value to assert equality with.
        value_2 : `Any`
            The second value to assert equality with.
        """
        self = AssertionConditionalBase.__new__(cls)
        
        self.value_1 = value_1
        
        self.state = CONDITION_STATES.CREATED
        
        return self.invoke()
    
    
    @copy_docs(AssertionConditionalBase._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in AssertionConditionalBase._cursed_repr_builder(self):
            
            repr_parts.append(', value_1=')
            repr_parts.append(repr(self.value_1))
            
            yield repr_parts


class AssertionConditionalBase2Value(AssertionConditionalBase1Value):
    """
    Base class for executing a two value assertion.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    value_1 : `Any`
        The value to call the condition on.
    value_2 : `Any`
        The value to call the condition with.
    """
    __slots__ = ('value_2',)
    
    def __new__(cls, value_1, value_2):
        """
        Asserts whether the two values are equal. Fails the test if not.
        
        Parameters
        ----------
        value_1 : `Any`
            First value to assert equality with.
        value_2 : `Any`
            The second value to assert equality with.
        """
        self = AssertionConditionalBase.__new__(cls)
        
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
