__all__ = ('FailureRaising',)

from .base import FailureBase

from scarletio import copy_docs


class FailureRaising(FailureBase):
    """
    Test failure representing a failed raising exception check.
    
    Attributes
    ----------
    handle : ``Handle``
        The test's handle running the test.
    expected_exceptions : `None`, `set` of `BaseException`
        Expected raised exceptions.
    expected_exact_type : `bool`
        Whether exception subclasses were allowed.
    exception_received : `None`, `BaseException`
        The received exception.
    """
    __slots__ = ('expected_exceptions', 'exceptions_exact_type', 'exception_received',)
    
    def __new__(cls, handle, expected_exceptions, exception_received, expected_exact_type):
        """
        Creates a new raising test failure.
        
        Parameters
        ----------
        handle : ``Handle``
            The test's handle running the test.
        expected_exceptions : `None`, `set` of `BaseException`
            Expected raised exceptions.
        exception_received : `None`, `BaseException`
            The received exception.
        expected_exact_type : `bool`
            Whether exception subclasses were allowed.
        """
        self = FailureBase.__new__(cls, handle)
        self.expected_exceptions = expected_exceptions
        self.expected_exact_type = expected_exact_type
        self.exception_received = exception_received
        return self
    
    
    @copy_docs(FailureBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(', expected_exceptions=')
        repr_parts.append(repr(self.expected_exceptions))
        
        repr_parts.append(', received_exception=')
        repr_parts.append(repr(self.exception_received))
        
        expected_exact_type = self.expected_exact_type
        if expected_exact_type:
            repr_parts.append(', expected_exact_type=')
            repr_parts.append(repr(expected_exact_type))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(FailureBase.get_failure_message)
    def get_failure_message(self):
        failure_message_parts = []
        failure_message_parts.append('Unexpected exception')
        
        # TODO
        
        return ''.join(failure_message_parts)
