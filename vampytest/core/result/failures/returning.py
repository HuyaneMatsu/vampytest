__all__ = ('FailureReturning',)

from scarletio import copy_docs

from .base import FailureBase
from .helpers import render_documentation_into, render_route_parts_into, render_parameters_into


class FailureReturning(FailureBase):
    """
    Test failure representing a bad return value.
    
    Attributes
    ----------
    handle : ``Handle``
        The test's handle running the test.
    expected_value : `None`, `object`
        The expected returned value.
    received_value : `None`, `object`
        The received returned value.
    """
    __slots__ = ('expected_value', 'received_value',)
    
    def __new__(cls, handle, expected_value, received_value):
        """
        Creates a new test failure representing a bad return value.
        
        Parameters
        ----------
        handle : ``Handle``
            The test's handle running the test.
        expected_value : `None`, `object`
            The expected returned value.
        received_value : `None`, `object`
            The received returned value.
        """
        self = FailureBase.__new__(cls, handle)
        self.expected_value = expected_value
        self.received_value = received_value
        return self
    
    
    @copy_docs(FailureBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(', expected_value = ')
        repr_parts.append(repr(self.expected_value))
        
        repr_parts.append(', received_value = ')
        repr_parts.append(repr(self.received_value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(FailureBase.get_failure_message)
    def get_failure_message(self):
        handle = self.handle
        
        failure_message_parts = []
        failure_message_parts.append('Unexpected return at: ')
        failure_message_parts = render_route_parts_into(failure_message_parts, handle)
        failure_message_parts = render_documentation_into(failure_message_parts, handle)
        
        
        final_call_state = handle.final_call_state
        if (final_call_state is not None) and final_call_state:
            failure_message_parts.append('\nParameters: ')
            failure_message_parts = render_parameters_into(
                failure_message_parts, final_call_state.positional_parameters, final_call_state.keyword_parameters
            )
        
        failure_message_parts.append('\nExpected return: ')
        failure_message_parts.append(repr(self.expected_value))
        
        failure_message_parts.append('\nReceived return: ' )
        failure_message_parts.append(repr(self.received_value))
        
        
        return ''.join(failure_message_parts)
