__all__ = ('WrapperReverse',)

from scarletio import copy_docs

from .wrapper_base import WrapperBase


class WrapperReverse(WrapperBase):
    """
    Reverses the test's result.

    Attributes
    ----------
    wrapped : `None`, `object`
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
        return (1 << 4)
    
    
    @copy_docs(WrapperBase.do_reverse)
    def do_reverse(self):
        return True
