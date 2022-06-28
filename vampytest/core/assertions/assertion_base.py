__all__ = ('AssertionBase',)

from . import assertion_states as CONDITION_STATES
from .assertion_states import get_assertion_state_name

from scarletio import RichAttributeErrorBaseType


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
        self.state = CONDITION_STATES.NONE
        return self
    
    
    def _cursed_repr_builder(self):
        """
        Representation builder helper.
        
        This method is a generator.
        
        Examples
        --------
        ```
        for repr_parts in self._cursed_repr_builder():
            repr_parts.append(', oh no')
        
        return ''.join(repr_parts)
        ```
        """
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' state=')
        repr_parts.append(get_assertion_state_name(self.state))
        
        yield repr_parts
        
        repr_parts.append('>')
    
    
    def __repr__(self):
        """Returns the condition's representation."""
        for repr_parts in self._cursed_repr_builder():
            pass
        
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
