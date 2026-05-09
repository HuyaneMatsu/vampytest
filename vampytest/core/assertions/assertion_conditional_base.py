__all__ = ('AssertionConditionalBase', 'AssertionConditionalBase1Value', 'AssertionConditionalBase2Value')

from scarletio import copy_docs, include

from .assertion_base import AssertionBase
from .assertion_states import ASSERTION_STATE_CREATED, ASSERTION_STATE_PASSED, ASSERTION_STATE_FAILED


AssertionException = include('AssertionException')


class AssertionConditionalBase(AssertionBase):
    """
    Base class for conditional assertions.
    
    Attributes
    ----------
    exception : `None | BaseException`
        Exception raised by the condition if any.
    
    reverse : `bool`
        Whether the condition should be reversed.
    
    state : `str`
        The condition's state.
    """
    __slots__ = ('reverse')
    
    def __new__(cls, *, reverse = False):
        """
        Creates an new conditional assertion instance.
        
        Parameters
        ----------
        reverse : `bool` = `False`, Optional (Keyword only)
            Whether the condition should be reversed.
        """
        self = AssertionBase.__new__(cls)
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
        
        except BaseException as exception:
            self.state = ASSERTION_STATE_FAILED
            self.exception = exception
            
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


class AssertionConditionalBase1Value(AssertionConditionalBase):
    """
    Base class for executing a one value assertion.
    
    Attributes
    ----------
    state : `int`
        The condition's state.
    
    exception : `None | BaseException`
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
            The value to assert with.
        
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


class AssertionConditionalBase2Value(AssertionConditionalBase1Value):
    """
    Base class for executing a two value assertion.
    
    Attributes
    ----------
    state : `int`
        The condition's state.
    
    exception : `None | BaseException`
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
            The first value to assert with.
        
        value_1 : `object`
            The second value to assert with.
        
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
