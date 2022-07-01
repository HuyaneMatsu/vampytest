__all__ = ('EventBase',)

from .constants import IDENTIFIER_NONE

from scarletio import RichAttributeErrorBaseType, copy_docs


class EventBase(RichAttributeErrorBaseType):
    """
    Represents a dispatched event by a test runner.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test running context.
    """
    __slots__ = ('context',)
    
    identifier = IDENTIFIER_NONE
    
    def __new__(cls, context):
        """
        Creates a new event instance.
        
        Parameters
        ----------
        context : ``RunnerContext``
            The respective test running context.
        """
        self = object.__new__(cls)
        self.context = context
        return self
    
    
    def __repr__(self):
        """Returns the representation of the event."""
        return f'<{self.__class__.__name__}>'


class FileEventBase(EventBase):
    """
    Represents a dispatched event by a test runner.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test running context.
    file : ``TestFile``
        The respective test file.
    """
    __slots__ = ('file',)
    
    def __new__(cls, context, file):
        """
        Creates a new file event instance.
        
        Parameters
        ----------
        context : ``RunnerContext``
            The respective test running context.
        file : ``TestFile``
            The respective test file.
        """
        self = EventBase.__new__(cls, context)
        self.file = file
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} file={self.file!r}>'


class ResultGroupEventBase(EventBase):
    """
    Represents a dispatched event by a test runner.
    
    Attributes
    ----------
    context : ``RunnerContext``
        The respective test running context.
    result_group : ``ResultGroup``
        The respective result group.
    """
    __slots__ = ('result_group',)
    
    def __new__(cls, context, result_group):
        """
        Creates a new file event instance.
        
        Parameters
        ----------
        context : ``RunnerContext``
            The respective test running context.
        result_group : ``ResultGroup``
            The respective result group.
        """
        self = EventBase.__new__(cls, context)
        self.result_group = result_group
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} result_group={self.result_group!r}>'
