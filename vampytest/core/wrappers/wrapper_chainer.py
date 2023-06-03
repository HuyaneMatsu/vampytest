__all__ = ('WrapperChainer',)

from scarletio import copy_docs, export

from ..helpers.hashing import hash_set

from .wrapper_base import WrapperBase


@export
class WrapperChainer(WrapperBase):
    """
    Attributes
    ----------
    wrapped : `None`, `object`
        The wrapped test.
    wrappers : `set` of ``WrapperBase``
        The applied wrappers.
    """
    __slots__ = ('wrappers',)
    
    def __new__(cls, wrapped = None):
        """
        Creates a new combined wrapper containing more wrappers.
        
        Parameters
        ----------
        wrapped : `None`, `object` = `None`, Optional
            The wrapped test if any.
        """
        self = object.__new__(cls)
        self.wrapped = wrapped
        self.wrappers = set()
        return self
    
    
    @copy_docs(WrapperBase.__call__)
    def __call__(self, to_wrap):
        if isinstance(to_wrap, WrapperBase):
            self.append(to_wrap)
            return self
        
        
        if (self.wrapped is not None):
            raise RuntimeError(f'Wrapped already wrapped; self = {self!r}, to_wrap = {to_wrap!r}.')
        
        self.wrapped = to_wrap
        return self
    
    
    @copy_docs(WrapperBase.__repr__)
    def __repr__(self):
        for field_added, repr_parts in self._cursed_repr_builder():
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' wrappers = ')
            repr_parts.append(repr(self.wrappers))
        
        return ''.join(repr_parts)
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        hash_value = WrapperBase.__hash__(self)
        hash_value ^= hash_set(self.wrappers)
        return hash_value
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.wrappers != other.wrappers:
            return False
        
        return True
    
    
    @copy_docs(WrapperBase.do_skip)
    def do_skip(self):
        for wrapper in self.wrappers:
            if wrapper.do_skip():
                return True
        
        return False
    
    
    @copy_docs(WrapperBase.do_reverse)
    def do_reverse(self):
        for wrapper in self.wrappers:
            if wrapper.do_reverse():
                return True
        
        return False
    
    @copy_docs(WrapperBase.check_conflicts)
    def check_conflicts(self):
        wrappers = list(self.wrappers)
        for wrapper in wrappers:
            wrapper_conflict = wrapper.check_conflicts()
            if (wrapper_conflict is not None):
                return wrapper_conflict
        
        
        while True:
            wrapper_to_check = wrappers.pop()
            
            if not wrappers:
                break
            
            for wrapper in wrappers:
                wrapper_conflict = wrapper_to_check.check_conflict_with(wrapper)
                if (wrapper_conflict is not None):
                    return wrapper_conflict
    
    
    @copy_docs(WrapperBase.iter_wrappers)
    def iter_wrappers(self):
        for wrapper in self.wrappers:
            yield from wrapper.iter_wrappers()
    
    
    @copy_docs(WrapperBase.iter_environments)
    def iter_environments(self):
        for wrapper in self.wrappers:
            yield from wrapper.iter_environments()
    
    
    def append(self, wrapper):
        """
        Adds a new wrapper to chain up.
        
        Parameters
        ----------
        wrapper : ``WrapperBase``
            The wrapper to extend self with.
        """
        if isinstance(wrapper, WrapperChainer):
            for sub_wrapper in wrapper.wrappers:
                self.append(sub_wrapper)
            
            return
        
        
        self.wrappers.add(wrapper)
