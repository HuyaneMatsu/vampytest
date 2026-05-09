__all__ = ('AssertionBase',)

from scarletio import RichAttributeErrorBaseType

from .assertion_states import ASSERTION_STATE_NONE, get_assertion_state_name


class AssertionBase(RichAttributeErrorBaseType):
    """
    Base class for conditions.
    
    Attributes
    ----------
    exception : `None | BaseException`
        Exception raised within the assertion.
    
    state : `int`
        The condition's state.
    """
    __slots__ = ('exception', 'state',)
    
    
    def __new__(cls):
        """
        Creates a new condition.
        """
        self = object.__new__(cls)
        self.exception = None
        self.state = ASSERTION_STATE_NONE
        return self
    
    
    def _build_repr_parts_into(self, into):
        """
        Representation builder helper.
        
        Parameters
        ----------
        into : `list<str>`
            List of strings to build the representation into.
        
        Returns
        -------
        into : `list<str>`
        """    
        exception = self.exception
        if (exception is not None):
            into.append(', exception = ')
            into.append(repr(exception))
        
        return into
    
    
    def __repr__(self):
        """Returns the condition's representation."""
        repr_parts = ['<', type(self).__name__]
        repr_parts.append(' state = ')
        repr_parts.append(get_assertion_state_name(self.state))
        repr_parts = self._build_repr_parts_into(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)
