__all__ = ('SourceLoadFailureEvent',)

from scarletio import copy_docs

from .base import EventBase
from .constants import IDENTIFIER_SOURCE_LOAD_FAILURE


class SourceLoadFailureEvent(EventBase):
    """
    Dispatched when a test file's all tests ran.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test runner context.
    exception : ``BaseException``
        The occurred exception.
    source : `str`
        The source's name.
    """
    __slots__ = ('exception', 'source')
    
    identifier = IDENTIFIER_SOURCE_LOAD_FAILURE

    def __new__(cls, context, source, exception):
        """
        Creates a new file sy instance.
        
        Parameters
        ----------
        context : ``RunnerContext``
            The respective test running context.
        source : `str`
            The source's name.
        exception : ``BaseException``
            The occurred exception.
        """
        self = object.__new__(cls)
        self.context = context
        self.exception = exception
        self.source = source
        return self
    

    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' source = ')
        repr_parts.append(repr(self.source))
        
        repr_parts.append(', exception = ')
        repr_parts.append(repr(self.exception))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
