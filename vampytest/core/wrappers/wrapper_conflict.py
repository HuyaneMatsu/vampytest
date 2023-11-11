__all__ = ('WrapperConflict',)

from scarletio import RichAttributeErrorBaseType


class WrapperConflict(RichAttributeErrorBaseType):
    """
    Raised when 2 wrappers have conflict with each other.
    
    Attributes
    ----------
    wrapper_0 : ``WrapperBase``
        The wrapper 1 with the conflict.
    reason : `None`, `str`
        The reason why the two wrappers are incompatible.
    wrapper_1 : `None`, ``WrapperBase``
        The wrapper 2 with the conflict.
    """
    __slots__ = ('reason', 'wrapper_0', 'wrapper_1')
    
    def __new__(cls, wrapper_0, wrapper_1 = None, *, reason = None):
        """
        Creates a new wrapper conflict.
        
        Parameters
        ----------
        wrapper_0 : ``WrapperBase``
            Wrapper one with the conflict.
        wrapper_1 : `None`, ``WrapperBase`` = `None`, Optional
            Wrapper two with the conflict.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            The reason why the two wrappers are incompatible.
        """
        self = object.__new__(cls)
        self.wrapper_0 = wrapper_0
        self.wrapper_1 = wrapper_1
        self.reason = reason
        return self
    
    
    def __repr__(self):
        """Returns the wrapper conflict's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' wrapper_0 = ')
        repr_parts.append(repr(self.wrapper_0))
        
        wrapper_1 = self.wrapper_1
        if (wrapper_1 is not None):
            repr_parts.append(', wrapper_1 = ')
            repr_parts.append(repr(self.wrapper_1))
        
        reason = self.reason
        if (reason is not None):
            repr_parts.append(', reason = ')
            repr_parts.append(repr(self.reason))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the wrapper conflict's hash value."""
        hash_value = 0
        
        hash_value ^= hash(self.wrapper_0)
        
        wrapper_1 = self.wrapper_1
        if (wrapper_1 is not None):
            hash_value ^= hash(wrapper_1)
        
        reason = self.reason
        if (reason is not None):
            hash_value ^= hash(reason)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two wrapper conflicts are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.wrappers != other.wrappers:
            return False
        
        if self.reason != other.reason:
            return False
        
        return True
    
    
    @property
    def wrappers(self):
        """
        Returns the collective wrappers of the conflict.
        
        Returns
        -------
        wrappers : `frozenset` of ``WrapperBase``
        """
        wrappers = [self.wrapper_0]
        
        wrapper_1 = self.wrapper_1
        if (wrapper_1 is not None):
            wrappers.append(wrapper_1)
        
        return frozenset(wrappers)
