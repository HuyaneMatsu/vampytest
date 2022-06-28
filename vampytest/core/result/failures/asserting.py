__all__ = ('FailureAsserting',)

from .base import FailureBase
from .helpers import add_documentation_into, add_route_parts_into

from scarletio import copy_docs


class FailureAsserting(FailureBase):
    """
    Test failure representing a failed assertion.
    
    Attributes
    ----------
    handle : ``Handle``
        The test's handle running the test.
    assertion : ``AssertionBase``
        The failed assertion.
    """
    __slots__ = ('assertion',)
    
    def __new__(cls, handle, assertion):
        """
        Creates a new assertion test failure.
        
        Parameters
        ----------
        handle : ``Handle``
            The test's handle running the test.
        assertion : ``AssertionBase``
            The failed assertion.
        """
        self = FailureBase.__new__(cls, handle)
        self.assertion = assertion
        return self
    
    
    @copy_docs(FailureBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' assertion')
        repr_parts.append(repr(self.assertion))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(FailureBase.get_failure_message)
    def get_failure_message(self):
        
        failure_message_parts = []
        failure_message_parts.append('Assertion failed at: ')
        add_route_parts_into(self.handle,  failure_message_parts)
        
        add_documentation_into(self.handle, failure_message_parts)
        
        failure_message_parts.append('\n')
        failure_message_parts.append(repr(self.assertion))
        
        return ''.join(failure_message_parts)
