__all__ = ('AssertionRaising', 'assert_raises')

from ..helpers import try_match_exception, un_nest_expected_exceptions

from . import assertion_states as CONDITION_STATES
from .assertion_base import AssertionBase
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
    expected_exceptions : `set` of ``BaseException``
        The expected exception types.
    
    Examples
    --------
    ```py
    with AssertionRaising(TypeError):
        'nice' + 69
    ```
    """
    __slots__ = ('accept_subtypes', 'exception', 'expected_exceptions')
    
    def __new__(cls, *expected_exceptions, accept_subtypes=True):
        """
        Creates a new raise asserting context manager.
        
        Parameters
        ----------
        *expected_exceptions : tuple` of (`BaseException`, ...)
            Exception types to expect.
        accept_subtypes : `bool` = `True`
            Whether subclasses are accepted as well.
        
        Raises
        ------
        TypeError
            If an `expected_exceptions`'s type is incorrect.
        ValueError
            If no exception was passed.
        """
        expected_exceptions = un_nest_expected_exceptions(expected_exceptions)
        if not expected_exceptions:
            raise ValueError('At least 1 exception is required.')
        
        self = AssertionBase.__new__(cls)
        self.expected_exceptions = expected_exceptions
        self.accept_subtypes = accept_subtypes
        
        return self
    
    
    def __enter__(self):
        """Enters as context manager."""
        self.state = CONDITION_STATES.CREATED
        return None
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the context manager."""
        if exc_type is None:
            self.state = CONDITION_STATES.FAILED
            try:
                raise AssertionException(self)
            finally:
                # Clear reference to self
                self = None
        
        self.exception = exc_val
        
        if try_match_exception(self.expected_exceptions, exc_val, self.accept_subtypes):
            state = CONDITION_STATES.PASSED
            silence = True
        
        else:
            state = CONDITION_STATES.FAILED
            silence = False
        
        self.state = state
        return silence


assert_raises = AssertionRaising
