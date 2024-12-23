__all__ = ('ContextCalling',)

from scarletio import copy_docs, include

from ..helpers.exception_matching import try_match_exception

from .base import ContextBase


AssertionException = include('AssertionException')
Result = include('Result')
ResultState = include('ResultState')


class ContextCalling(ContextBase):
    """
    Base test context.

    Attributes
    ----------
    handle : ``Handle``
        The parent handle.
    wrapper_calling : ``WrapperCalling``
        The wrapper that defines the input and output of the test.
    """
    __slots__ = ('handle', 'wrapper_calling')
    
    def __new__(cls, handle, wrapper_calling):
        """
        Creates a new test context.
        
        Parameters
        ----------
        handle : ``Handle``
            The parent handle.
        wrapper_calling : ``WrapperCalling``
            The wrapper that defines the input and output of the test.
        """
        self = object.__new__(cls)
        self.handle = handle
        self.wrapper_calling = wrapper_calling
        return self
    
    
    @copy_docs(ContextBase.__repr__)
    def __repr__(self):
        return ''.join(['<', type(self).__name__, '>'])
    
    
    @copy_docs(ContextBase.enter)
    def enter(self, call_state):
        wrapper_calling = self.wrapper_calling
        if wrapper_calling.is_call_with():
            call_state = call_state.with_parameters(
                wrapper_calling.calling_positional_parameters,
                wrapper_calling.calling_keyword_parameters,
            )
        
        return (None, call_state)
    
    
    @copy_docs(ContextBase.exit)
    def exit(self, result_state):
        wrapper_calling = self.wrapper_calling
        
        if (result_state is None) or (not result_state.is_raise()):
            raised_exception = None
        else:
            raised_exception = result_state.result
        
        result = None
        
        if (raised_exception is None) or (not isinstance(raised_exception, AssertionException)):
            handle = self.handle
            
            if wrapper_calling.is_raising():
                raising_exceptions = wrapper_calling.raising_exceptions
                raising_accept_subtypes = wrapper_calling.raising_accept_subtypes
                
                if raised_exception is None:
                    result = Result(
                        handle.case
                    ).with_handle(
                        handle
                    ).with_exception(
                        raising_exceptions, raising_accept_subtypes, None,
                    )
                
                else:
                    if try_match_exception(
                        raising_exceptions, raised_exception, raising_accept_subtypes, wrapper_calling.raising_where
                    ):
                        if (result_state is not None):
                            result_state = ResultState()
                    
                    else:
                        result = Result(
                            handle.case
                        ).with_handle(
                            handle
                        ).with_exception(
                            raising_exceptions, raising_accept_subtypes, raised_exception,
                        )
            
            elif wrapper_calling.is_returning():
                if (raised_exception is not None):
                    result = Result(handle.case).with_handle(handle).with_exception(None, False, raised_exception)
                
                else:
                    if (result_state is None) or (not result_state.is_return()):
                        returned_value = None
                    else:
                        returned_value = result_state.result
                    
                    returning_value = wrapper_calling.returning_value
                    
                    if returned_value != returning_value:
                        result = Result(handle.case).with_handle(handle).with_return(returning_value, returned_value)
        
        return result, result_state
