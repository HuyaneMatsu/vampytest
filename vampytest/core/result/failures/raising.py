__all__ = ('FailureRaising',)

from ...environment.default import __file__ as VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH
from ...environment.scarletio_coroutine import __file__ as VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH

from .base import FailureBase
from .helpers import add_documentation_into, add_route_parts_into, render_parameters_into

from scarletio import copy_docs, render_exception_into


def ignore_invoke_test_frame(file_name, name, line_number, line):
    """
    Ignores the frame where the test is called from.
    
    Parameters
    ----------
    file_name : `str`
        The frame's respective file's name.
    name : `str`
        The frame's respective function's name.
    line_number : `int`
        The line's index where the exception occurred.
    line : `str`
        The frame's respective stripped line.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    if file_name == VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH:
        if name == 'run':
            if line == 'returned_value = test(*positional_parameters, **keyword_parameters)':
                should_show_frame = False
    
    elif file_name == VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH:
        if name == '_run_async':
            if line == 'returned_value = await test(*positional_parameters, **keyword_parameters)':
                should_show_frame = False
    
    return should_show_frame


class FailureRaising(FailureBase):
    """
    Test failure representing a failed raising exception check.
    
    Attributes
    ----------
    handle : ``Handle``
        The test's handle running the test.
    accept_subtypes : `bool`
        Whether exception subclasses were allowed.
    expected_exceptions : `None`, `set` of `BaseException`
        Expected raised exceptions.
    exception_received : `None`, `BaseException`
        The received exception.
    """
    __slots__ = ('accept_subtypes', 'expected_exceptions', 'exception_received',)
    
    def __new__(cls, handle, expected_exceptions, exception_received, accept_subtypes):
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
        accept_subtypes : `bool`
            Whether exception subclasses were allowed.
        """
        self = FailureBase.__new__(cls, handle)
        self.expected_exceptions = expected_exceptions
        self.exception_received = exception_received
        self.accept_subtypes = accept_subtypes
        return self
    
    
    @copy_docs(FailureBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(', expected_exceptions=')
        repr_parts.append(repr(self.expected_exceptions))
        
        repr_parts.append(', received_exception=')
        repr_parts.append(repr(self.exception_received))
        
        accept_subtypes = self.accept_subtypes
        if accept_subtypes:
            repr_parts.append(', accept_subtypes=')
            repr_parts.append(repr(accept_subtypes))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(FailureBase.get_failure_message)
    def get_failure_message(self):
        failure_message_parts = []
        
        failure_message_parts.append('Unexpected exception at: ')
        add_route_parts_into(self.handle, failure_message_parts)
        
        add_documentation_into(self.handle, failure_message_parts)
        
        failure_message_parts.append('\nParameters: ')
        render_parameters_into(self.handle.final_call_state, failure_message_parts)
        
        failure_message_parts.append('\nExpected return: ')
        expected_exceptions = self.expected_exceptions
        if expected_exceptions is None:
            failure_message_parts.append('N/A')
        
        else:
            exception_added = False
            
            for expected_exception in expected_exceptions:
                if exception_added:
                    failure_message_parts.append(', ')
                else:
                    exception_added = True
                
                if isinstance(expected_exception, type):
                    expected_exception_representation = expected_exception.__name__
                else:
                    expected_exception_representation = repr(expected_exception)
                
                failure_message_parts.append(expected_exception_representation)
            
            failure_message_parts.append('\nAccept sub-classes: ')
            failure_message_parts.append('true' if self.accept_subtypes else 'false')
        
        
        failure_message_parts.append('\nReceived return:')
        exception_received = self.exception_received
        if (exception_received is None):
            failure_message_parts.append('N/A')
        
        else:
            failure_message_parts.append('\n')
            failure_message_parts.append('-' * 80)
            failure_message_parts.append('\n')
            
            render_exception_into(exception_received, failure_message_parts, filter=ignore_invoke_test_frame)
        
        return ''.join(failure_message_parts)
