__all__ = ('WrapperBase', )

from ..helpers import hash_object


# Will be resolved later
WrapperChainer = NotImplemented


class WrapperBase:
    """
    Base class for test wrappers defining shared functionality.
    
    Attributes
    ----------
    wrapped : `None`, `Any`
        The wrapped test.
    """
    __slots__ = ('wrapped', )
    
    def __new__(cls):
        """
        Creates a new test wrapper.
        """
        self = object.__new__(cls)
        self.wrapped = None
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
        if isinstance(to_wrap, WrapperChainer):
            to_wrap.append(self)
            return to_wrap
        
        if isinstance(to_wrap, WrapperBase):
            wrapper_chainer = WrapperChainer(to_wrap.wrapped)
            wrapper_chainer.append(self)
            wrapper_chainer.append(to_wrap)
            return wrapper_chainer
        
        
        if (self.wrapped is not None):
            raise RuntimeError(f'Wrapped already wrapped; self={self!r}, to_wrap={to_wrap!r}.')
        
        self.wrapped = to_wrap
        return self
    
    
    def __matmul__(self, other):
        """Returns `self(other)`"""
        return self.__call__(other)
    
    
    def __rmatmul__(self, other):
        """Returns `self(other)`"""
        return self.__call__(other)
        
    
    def _cursed_repr_builder(self):
        """
        Representation builder helper.
        
        This method is a generator.
        
        Examples
        --------
        ```
        for field_added, repr_parts in self._cursed_repr_builder():
            if not field_added:
                repr_parts.append(',')
            
            repr_parts.append(' oh no')
        
        return "".join(repr_parts)
        ```
        """
        repr_parts = ['<', self.__class__.__name__]
        
        wrapped = self.wrapped
        if (wrapped is None):
            repr_parts.append(' wrapped=')
            repr_parts.append(repr(wrapped))
            
            field_added = True
        else:
            field_added = False
        
        yield field_added, repr_parts
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __repr__(self):
        """Returns the wrapper's representation."""
        for field_added, repr_parts in self._cursed_repr_builder():
            pass
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the wrapper's representation."""
        wrapped = self.wrapped
        if wrapped is None:
            hash_value = 0
        else:
            hash_value = hash_object(wrapped)
        
        return hash_value
    
    
    def __eq__(self, other):
        """return whether the two wrappers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.wrapped != other.wrapped:
            return False
        
        return True
    
    
    def do_skip(self):
        """
        Whether the test should be skipped.
        
        Returns
        -------
        do_skip : `bool`
            Always returns false.
        """
        return False
    
    
    def check_conflicts(self):
        """
        Checks whether the wrapper has internal conflict.
        
        Returns
        ------
        wrapper_conflict: `None`, ``WrapperConflict``
        """
        pass
    
    
    def check_conflict_with(self, other):
        """
        Checks whether the wrapper has conflict with the other one.
        
        Returns
        ------
        wrapper_conflict: `None`, ``WrapperConflict``
        """
        pass
    
    
    def has_bound_test(self):
        """
        Returns whether the wrapper wraps a test.
        
        Returns
        -------
        has_bound_test : `bool`
        """
        return (self.wrapped is not None)
    
    
    def unbind_test(self):
        """
        Unbinds the wrappers test.
        
        Returns
        -------
        test : `Any`
        
        Raises
        ------
        RuntimeError
            The wrapper had no test or already unbind.
        """
        wrapped = self.wrapped
        if wrapped is None:
            raise RuntimeError(f'The wrapper had no test or already unbind; self={self!r}.')
        
        self.wrapped = None
        return wrapped
