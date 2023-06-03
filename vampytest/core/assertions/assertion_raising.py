__all__ = ('AssertionRaising',)

from ..helpers.exception_matching import try_match_exception
from ..helpers.un_nesting import un_nest_exceptions

from .assertion_base import AssertionBase
from .assertion_states import ASSERTION_STATE_CREATED, ASSERTION_STATE_FAILED, ASSERTION_STATE_PASSED
from .exceptions import AssertionException



class AssertionRaising(AssertionBase):
    """
    Context manager, which checks for exception raise.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised within the context block if any.
    accept_subtypes : `bool`
        Whether subclasses are accepted as well.
    expected_exceptions : `set` of (`BaseException`, `type<BaseException>`)
        The expected exception types.
    
    Examples
    --------
    ```py
    with AssertionRaising(TypeError):
        'nice' + 69
    ```
    """
    __slots__ = ('accept_subtypes', 'exception', 'expected_exceptions')
    
    def __new__(cls, expected_exception, *expected_exceptions, accept_subtypes = True):
        """
        Creates a new raise asserting context manager.
        
        Parameters
        ----------
        expected_exception : `BaseException˙
            The expected exception to be raised.
        *expected_exceptions : ˙tuple<BaseException>˙
            Additional expected exceptions.
        accept_subtypes : `bool` = `True`, optional (Keyword only)
            Whether subclasses are accepted as well.
        
        Raises
        ------
        TypeError
            If an `expected_exceptions`'s type is incorrect.
        ValueError
            If no exception was passed.
        """
        expected_exceptions = un_nest_exceptions((expected_exception, *expected_exceptions))
        if not expected_exceptions:
            raise ValueError(
                'At least 1 exception is required.'
            )
        
        self = AssertionBase.__new__(cls)
        self.expected_exceptions = expected_exceptions
        self.accept_subtypes = accept_subtypes
        
        return self
    
    
    def __enter__(self):
        """Enters as context manager."""
        self.state = ASSERTION_STATE_CREATED
        return None
    
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        """Exits the context manager."""
        if exception_type is None:
            self.state = ASSERTION_STATE_FAILED
            try:
                raise AssertionException(self)
            finally:
                # Clear reference to self
                self = None
        
        self.exception = exception_value
        
        if try_match_exception(self.expected_exceptions, exception_value, self.accept_subtypes):
            state = ASSERTION_STATE_PASSED
            silence = True
        
        else:
            state = ASSERTION_STATE_FAILED
            silence = False
        
        self.state = state
        return silence
