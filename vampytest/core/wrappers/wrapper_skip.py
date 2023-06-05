__all__ = ('WrapperSkip',)

from scarletio import copy_docs

from .wrapper_base import WrapperBase


class WrapperSkip(WrapperBase):
    """
    Skips the test.

    Attributes
    ----------
    wrapped : `None`, `object`
        The wrapped test.
    """
    __slots__ = ()
    
    @copy_docs(WrapperBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__}'
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        return 1
    
    
    @copy_docs(WrapperBase.do_skip)
    def do_skip(self):
        return True
