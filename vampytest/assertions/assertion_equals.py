__all__ = ('AssertionEquals',)

from . import assertion_states as CONDITION_STATES
from .assertion_base import AssertionBase
from .exceptions import AssertionException

class AssertionEquals(AssertionBase):
    """
    Quality condition.
    """
    __slots__ = ('exception', 'parameter_1', 'parameter_2',)
    
    def __new__(cls, parameter_1, parameter_2):
        """
        Asserts whether the two values are equal. Fails the test if not.
        
        Parameters
        ----------
        parameter_1 : `Any`
            First parameter to assert equality with.
        parameter_2 : `Any`
            The second parameter to assert equality with.
        
        
        """
        self = object.__new__(cls)
        self.state = CONDITION_STATES.CREATED
        
        self.exception = None
        self.parameter_1 = parameter_1
        self.parameter_2 = parameter_2
        
        try:
            equality_return = parameter_1 == parameter_2
            
            if equality_return:
                passed = True
            else:
                passed = False
        
        except BaseException as err:
            self.state = CONDITION_STATES.FAILED
            self.exception = err
            
        else:
            if passed:
                self.state = CONDITION_STATES.PASSED
                return equality_return
            
            self.state = CONDITION_STATES.FAILED
        
        try:
            raise AssertionException(self)
        finally:
            # Remove self reference, so garbage collector wont fail
            self = None
    
    
    def __repr__(self):
        """Returns the representation of the equality condition."""
        for repr_parts in self._cursed_repr_builder():
            
            repr_parts.append(', parameter_1=')
            repr_parts.append(repr(self.parameter_1))
            
            repr_parts.append(', parameter_2=')
            repr_parts.append(repr(self.parameter_2))
            
            exception = self.exception
            if (exception is not None):
                repr_parts.append(', exception=')
                repr_parts.append(repr(self.exception))
        
        return "".join(repr_parts)
