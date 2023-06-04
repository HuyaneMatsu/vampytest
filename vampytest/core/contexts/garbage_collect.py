__all__ = ('ContextGarbageCollect',)

from gc import collect as gc_collect

from scarletio import copy_docs

from .base import ContextBase


class ContextGarbageCollect(ContextBase):
    """
    Garbage collection contexts that call `gc.collect`.

    Attributes
    ----------
    wrapper_garbage_collect : ``WrapperGarbageCollect``
        The wrapper that defines when should garbage collection happen.
    """
    __slots__ = ('wrapper_garbage_collect',)
    
    def __new__(cls, wrapper_garbage_collect):
        """
        Creates a new test context.
        
        Parameters
        ----------
        wrapper_garbage_collect : ``WrapperGarbageCollect``
            The wrapper that defines when should garbage collection happen.
        """
        self = object.__new__(cls)
        self.wrapper_garbage_collect = wrapper_garbage_collect
        return self
    
    
    @copy_docs(ContextBase.__repr__)
    def __repr__(self):
        return ''.join(['<', self.__class__.__name__, '>'])
    
    
    @copy_docs(ContextBase.start)
    def start(self):
        if self.wrapper_garbage_collect.before:
            gc_collect()
            gc_collect()
    
    
    @copy_docs(ContextBase.close)
    def close(self, result):
        if self.wrapper_garbage_collect.after:
            gc_collect()
            gc_collect()
