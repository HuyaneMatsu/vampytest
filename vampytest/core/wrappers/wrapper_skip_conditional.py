__all__ = ('WrapperSkipConditional', )

from scarletio import copy_docs

from .wrapper_skip import WrapperSkip


class WrapperSkipConditional(WrapperSkip):
    """
    Skips the test.

    Attributes
    ----------
    wrapped : `None`, `object`
        The wrapped test.
    skip : `bool`
        Whether the test should be skipped.
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
    
    
    @copy_docs(WrapperSkip.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} skip={self.skip}>'
    
    
    @copy_docs(WrapperSkip.__eq__)
    def __eq__(self, other):
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
    
    
    @copy_docs(WrapperSkip.__hash__)
    def __hash__(self):
        return self.skip
    
    
    @copy_docs(WrapperSkip.do_skip)
    def do_skip(self):
        return self.skip
