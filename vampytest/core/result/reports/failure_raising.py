__all__ = ('ReportFailureRaising',)

from scarletio import copy_docs

from .base import ReportBase


class ReportFailureRaising(ReportBase):
    """
    Test failure representing a failed raising exception check.
    
    Attributes
    ----------
    accept_subtypes : `bool`
        Whether exception subclasses were allowed.
    expected_exceptions : `None | set<type<BaseException> | instance<BaseException>>`
        Expected raised exceptions.
    exception_received : `None | BaseException`
        The received exception.
    """
    __slots__ = ('accept_subtypes', 'expected_exceptions', 'exception_received',)
    
    def __new__(cls, expected_exceptions, accept_subtypes, exception_received):
        """
        Creates a new raising test failure.
        
        Parameters
        ----------
        expected_exceptions : `None | set<type<BaseException> | instance<BaseException>>`
            Expected raised exceptions.
        accept_subtypes : `bool`
            Whether exception subclasses were allowed.
        exception_received : `None | BaseException`
            The received exception.
        """
        self = object.__new__(cls)
        self.expected_exceptions = expected_exceptions
        self.accept_subtypes = accept_subtypes
        self.exception_received = exception_received
        return self
    
    
    @copy_docs(ReportBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' expected_exceptions = ')
        repr_parts.append(repr(self.expected_exceptions))
        
        accept_subtypes = self.accept_subtypes
        if accept_subtypes:
            repr_parts.append(', accept_subtypes = ')
            repr_parts.append(repr(accept_subtypes))
        
        repr_parts.append(', exception_received = ')
        repr_parts.append(repr(self.exception_received))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ReportBase.is_failure)
    def is_failure(self):
        return True
