__all__ = ('FailureAsserting',)

from scarletio import copy_docs

from .base import FailureBase
from .helpers import render_documentation_into, render_route_parts_into, render_parameters_into


class FailureAsserting(FailureBase):
    """
    Test failure representing a failed assertion.
    
    Attributes
    ----------
    handle : ``Handle``
        The test's handle running the test.
    assertion_exception : ``AssertionException``
        The failed assertion.
    """
    __slots__ = ('assertion_exception',)
    
    def __new__(cls, handle, assertion_exception):
        """
        Creates a new assertion test failure.
        
        Parameters
        ----------
        handle : ``Handle``
            The test's handle running the test.
        assertion_exception : ``AssertionException``
            The failed assertion.
        """
        self = FailureBase.__new__(cls, handle)
        self.assertion_exception = assertion_exception
        return self
    
    
    @copy_docs(FailureBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' assertion')
        repr_parts.append(repr(self.assertion_exception))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(FailureBase.get_failure_message)
    def get_failure_message(self):
        handle = self.handle
        
        failure_message_parts = []
        failure_message_parts.append('Assertion failed at: ')
        failure_message_parts = render_route_parts_into(failure_message_parts, handle)
        failure_message_parts = render_documentation_into(failure_message_parts, handle)
        
        final_call_state = handle.final_call_state
        if (final_call_state is not None) and final_call_state:
            failure_message_parts.append('\nParameters: ')
            failure_message_parts = render_parameters_into(
                failure_message_parts, final_call_state.positional_parameters, final_call_state.keyword_parameters
            )
        
        failure_message_parts.append('\n')
        self.assertion_exception.render_failure_message_parts_into(failure_message_parts)
        
        return ''.join(failure_message_parts)
