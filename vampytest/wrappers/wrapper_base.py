__all__ = ('WrapperBase', )


class WrapperBase:
    """
    Base class for test wrappers defining shared functionality.
    
    Attributes
    ----------
    wrapped : `Any`
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
    
    
    def __repr__(self):
        """Returns the wrapper's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        wrapped = self.wrapped
        if (wrapped is not None):
            repr_parts.append(' wrapped=')
            repr_parts.append(repr(wrapped))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
