__all__ = ('WrapperChainer',)

from ..helpers import hash_set

from .wrapper_base import WrapperBase


class WrapperChainer(WrapperBase):
    """
    Attributes
    ----------
    wrapped : `None`, `Any`
        The wrapped test.
    wrappers : `set` of ``WrapperBase``
        The applied wrappers.
    """
    __slots__ = ('wrappers',)
    
    def __new__(cls, wrapped=None):
        """
        Creates a new combined wrapper containing more wrappers.
        
        Parameters
        ----------
        wrapped : `None`, `Any` = `None`, Optional
            The wrapped test if any.
        """
        self = object.__new__(cls)
        self.wrapped = wrapped
        self.wrappers = set()
        return self
    
    
    def __call__(self, to_wrap):
        """
        Calls the wrapper.
        
        Parameters
        ----------
        to_wrap : `Any`
            The object to wrap. It can be either a function or an another wrapper.
        
        Returns
        -------
        to_wrap : ``WrapperBase``
            The same or a newly created wrapper.
        
        Raises
        ------
        RuntimeError
            Wrapper already called.
        """
        if isinstance(to_wrap, WrapperBase):
            self.append(to_wrap)
            return self
        
        
        if (self.wrapped is not None):
            raise RuntimeError(f'Wrapped already wrapped; self={self!r}, to_wrap={to_wrap!r}.')
        
        self.wrapped = to_wrap
        return self
    
    
    def __repr__(self):
        """Returns the wrapper chainer's representation."""
        for field_added, repr_parts in self._cursed_repr_builder():
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' wrappers=')
            repr_parts.append(repr(self.wrappers))
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the wrapper chainer's hash value."""
        hash_value = WrapperBase.__hash__(self)
        hash_value ^= hash_set(self.wrappers)
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two wrapper chainers are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.wrappers != other.wrappers:
            return False
        
        return True
    
    
    def do_skip(self):
        """
        Whether the test should be skipped.
        
        Returns
        -------
        do_skip : `bool`
        """
        for wrapper in self.wrappers:
            if wrapper.do_skip():
                return True
        
        return False
    
    
    def check_conflicts(self):
        """
        Checks whether the wrapper has internal conflict.
        
        Chained wrappers check conflicts within themselves.
        
        Returns
        ------
        wrapper_conflict : `None`, ``WrapperConflict``
        """
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


# Resolve circular imports

from .import wrapper_base
wrapper_base.WrapperChainer = WrapperChainer
del wrapper_base
