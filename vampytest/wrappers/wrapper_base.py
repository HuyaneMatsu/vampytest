__all__ = ('WrapperBase', )

from .helpers import hash_object

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
        if (self.wrapped is not None):
            raise RuntimeError(f'Wrapped already wrapped; self={self!r}, to_wrap={to_wrap!r}.')
        
        if isinstance(to_wrap, WrapperChainer):
            to_wrap.append(self)
            return to_wrap
        
        if isinstance(to_wrap, WrapperBase):
            wrapper_chainer = WrapperChainer(to_wrap.wrapped)
            wrapper_chainer.append(self)
            wrapper_chainer.append(to_wrap)
            return wrapper_chainer
        
        self.wrapped = to_wrap
        return self
    
    
    def __matmul__(self, other):
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
