__all__ = ('AssertionBase',)

from scarletio import RichAttributeErrorBaseType

from .assertion_states import ASSERTION_STATE_NONE, get_assertion_state_name


class AssertionBase(RichAttributeErrorBaseType):
    """
    Base class for conditions.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    """
    __slots__ = ('state',)
    
    
    def __new__(cls):
        """
        Creates a new condition.
        """
        self = object.__new__(cls)
        self.state = ASSERTION_STATE_NONE
        return self
    
    
    def _build_repr_parts_into(self, into):
        """
        Representation builder helper.
        
        Parameters
        ----------
        into : `list` of `str`
            List of strings to build the representation into.
        
        Returns
        -------
        into : `list` of `str`
        """
        return into
    
    
    def __repr__(self):
        """Returns the condition's representation."""
        repr_parts = ['<', self.__class__.__name__]
        repr_parts.append(' state = ')
        repr_parts.append(get_assertion_state_name(self.state))
        repr_parts = self._build_repr_parts_into(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def render_failure_message_parts_into(self, failure_message_parts):
        """
        Renders the assertion into the given list.
        
        Parameters
        ----------
        failure_message_parts : `list` of `str`
            A list to extend with the rendered strings.
        
        Returns
        -------
        failure_message_parts : `list` of `str`
        """
        return failure_message_parts
