__all__ = ('ReportFailureReturning',)

from scarletio import copy_docs

from .base import ReportBase


class ReportFailureReturning(ReportBase):
    """
    Test failure representing a bad return value.
    
    Attributes
    ----------
    expected_value : `None | object`
        The expected returned value.
    received_value : `None | object`
        The received returned value.
    """
    __slots__ = ('expected_value', 'received_value',)
    
    def __new__(cls, expected_value, received_value):
        """
        Creates a new test failure representing a bad return value.
        
        Parameters
        ----------
        expected_value : `None | object`
            The expected returned value.
        received_value : `None | object`
            The received returned value.
        """
        self = object.__new__(cls)
        self.expected_value = expected_value
        self.received_value = received_value
        return self
    
    
    @copy_docs(ReportBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' expected_value = ')
        repr_parts.append(repr(self.expected_value))
        
        repr_parts.append(', received_value = ')
        repr_parts.append(repr(self.received_value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ReportBase.is_failure)
    def is_failure(self):
        return True
