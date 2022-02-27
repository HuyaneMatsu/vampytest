__all__ = ('WrapperSkip',)

from .wrapper_base import WrapperBase

from scarletio import copy_docs


class WrapperSkip(WrapperBase):
    """
    Skips the test.

    Attributes
    ----------
    wrapped : `None`, `Any`
        The wrapped test.
    """
    __slots__ = ()
    
    @copy_docs(WrapperBase.__repr__)
    def __repr__(self):
        """Returns the conditional skip wrapper's representation."""
        return f'<{self.__class__.__name__}'
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        """Returns whether the two conditional skip wrappers are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        """Returns the skip wrapper's hash value."""
        return 1
    
    
    @copy_docs(WrapperBase.do_skip)
    def do_skip(self):
        return True
