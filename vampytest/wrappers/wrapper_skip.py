__all__ = ('WrapperSkip',)

from .wrapper_base import WrapperBase

class WrapperSkip(WrapperBase):
    """
    Skips the test.

    Attributes
    ----------
    wrapped : `None`, `Any`
        The wrapped test.
    """
    __slots__ = ()
    
    def __repr__(self):
        """Returns the conditional skip wrapper's representation."""
        return f'<{self.__class__.__name__} skip={self.skip}>'
    
    
    def __eq__(self, other):
        """Returns whether the two conditional skip wrappers are the same."""
        if type(self) is type(other):
            if self.skip != other.skip:
                return False
            
            return True
        
        if type(other) is WrapperSkip:
            if not self.skip:
                return False
            
            return True
        
        return NotImplemented
    
    
    def __hash__(self):
        """Returns the skip wrapper's hash value."""
        return 1
    
    
    def do_skip(self):
        """
        Whether the test should be skipped.
        
        Returns
        -------
        do_skip : `bool`
            Always returns true.
        """
        return True
