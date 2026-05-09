__all__ = ('ReportFailureAsserting',)

from scarletio import copy_docs

from .base import ReportBase


class ReportFailureAsserting(ReportBase):
    """
    Test failure representing a failed assertion.
    
    Attributes
    ----------
    assertion_exception : ``AssertionException``
        The assertion's exception.
    """
    __slots__ = ('assertion_exception',)
    
    def __new__(cls, assertion_exception):
        """
        Creates a new assertion test failure.
        
        Parameters
        ----------
        assertion_exception : ``AssertionException``
            The assertion's exception.
        """
        self = object.__new__(cls)
        self.assertion_exception = assertion_exception
        return self
    
    
    @copy_docs(ReportBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' assertion_exception = ')
        repr_parts.append(repr(self.assertion_exception))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ReportBase.is_failure)
    def is_failure(self):
        return True
