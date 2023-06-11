__all__ = ('WrapperGarbageCollect',)

from scarletio import copy_docs

from ..contexts import ContextGarbageCollect

from .wrapper_base import WrapperBase


class WrapperGarbageCollect(WrapperBase):
    """
    Collects garbage before and (or) after the test as configured.
    
    Attributes
    ----------
    wrapped : `None`, `object`
        The wrapped test.
    after : `bool`
        Whether garbage should be collected after the test.
    before : `bool`
        Whether garbage should be collected before the test.
    """
    __slots__ = ('after', 'before')
    
    def __new__(cls, *, after = False, before = False):
        """
        Creates a new garbage collect wrapper.
        
        Parameters
        ----------
        after : `bool` = `False`, Optional (Keyword only)
            Whether garbage should be collected after the test.
        before : `bool` = `False`, Optional (Keyword only)
            Whether garbage should be collected before the test.
        
        Raises
        ------
        TypeError
            - If `after`'s type is incorrect.
            - If `before`'s type is incorrect.
        """
        if isinstance(after, bool):
            pass
        elif isinstance(after, int):
            after = True if after else False
        else:
            raise TypeError(
                f'`after` can be `bool`, got {after.__class__.__name__}; {after!r}.'
            )
        
        if isinstance(before, bool):
            pass
        elif isinstance(before, int):
            before = True if before else False
        else:
            raise TypeError(
                f'`before` can be `bool`, got {before.__class__.__name__}; {before!r}.'
            )
        
        self = WrapperBase.__new__(cls)
        self.after = after
        self.before = before
        return self
    
    
    @copy_docs(WrapperBase.get_context)
    def get_context(self, handle):
        return ContextGarbageCollect(self)
    
    
    @copy_docs(WrapperBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} before = {self.before!r}, after = {self.after!r}>'
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.after != other.after:
            return False
        
        if self.before != other.before:
            return False
        
        return True
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        return self.after ^ (self.before << 1)
