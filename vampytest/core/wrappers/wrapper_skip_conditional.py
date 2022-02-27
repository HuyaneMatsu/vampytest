__all__ = ('WrapperSkipConditional', )

from .wrapper_skip import WrapperSkip


class WrapperSkipConditional(WrapperSkip):
    """
    Skips the test.

    Attributes
    ----------
    wrapped : `None`, `Any`
        The wrapped test.
    """
    __slots__ = ('skip', )
    
    def __new__(cls, skip):
        """
        Creates a new conditional skip wrapper.
        
        Parameters
        ----------
        skip : `bool`
            Whether the test should be skipped.
        """
        skip = bool(skip)
        
        self = WrapperSkip.__new__(cls)
        self.skip = skip
        return self
    
    
    def __repr__(self):
        """Returns the conditional skip wrapper's representation."""
        return f'<{self.__class__.__name__} skip={self.skip}>'
    
    
    def __eq__(self, other):
        """Returns whether the two conditional skip wrappers are the same."""
        if type(self) is type(other):
            if self.wrapped != other.wrapped:
                return False
            
            if self.skip != other.skip:
                return False
            
            return True
        
        if type(other) is WrapperSkip:
            if self.wrapped != other.wrapped:
                return False
            
            if not self.skip:
                return False
            
            return True
        
        return NotImplemented
    
    
    def __hash__(self):
        """Returns the condition skip wrapper's hash value."""
        return self.skip
    
    
    def do_skip(self):
        """
        Whether the test should be skipped.
        
        Returns
        -------
        do_skip : `bool`
        """
        return self.skip
