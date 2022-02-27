__all__ = ('AssertionConditionalBase', )

from . import assertion_states as CONDITION_STATES
from .assertion_base import AssertionBase
from .exceptions import AssertionException


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
    
    
    def _cursed_repr_builder(self):
        """
        Representation builder helper.
        
        This method is a generator.
        """
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
        
        Subclasses should overwrite this method.
        
        Raises
        ------
        NotImplemented
        """
        raise NotImplemented
