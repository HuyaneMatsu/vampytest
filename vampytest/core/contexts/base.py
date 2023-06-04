__all__ = ()

from scarletio import RichAttributeErrorBaseType


class ContextBase(RichAttributeErrorBaseType):
    """
    Base test context.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new test context.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the context's representation."""
        return ''.join(['<', self.__class__.__name__, '>'])
    
    
    def start(self):
        """
        Starts the test context. If the test should already end returns a ``Result`` instance.
        
        Returns
        -------
        result : `None`, ``Result``
        """
        return None
    
    
    def enter(self, call_state):
        """
        Enters the context.
        
        Parameters
        ----------
        call_state : ``CallState``
            Call state of the test to modify.
            
        Returns
        -------
        result : `None`, ``Result``
            Test result to propagate.
        call_state : `None`, ``CallState``
            New call state to use.
        """
        return (None, None)
    
    
    def exit(self, result_state):
        """
        Exists the context.
        
        Parameters
        ----------
        result_state : ``ResultState``
            Result state of the test to modify.
        
        Returns
        -------
        result : `None`, ``Result``
            Test result to propagate.
        result_state : ``ResultState``
            New result state to use.
        """
        return (None, None)
    
    
    def close(self, result):
        """
        Closes the test context.
        
        Parameters
        ----------
        result : `None`, ``Result``
            Result of the test. Passed as `None` if an exception occurred while handling the test.
        """
        return None
