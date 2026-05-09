__all__ = ('AssertionRaising',)

from scarletio import copy_docs, include

from ..helpers.exception_matching import try_match_exception
from ..helpers.un_nesting import un_nest_exceptions

from .assertion_base import AssertionBase
from .assertion_states import ASSERTION_STATE_CREATED, ASSERTION_STATE_FAILED, ASSERTION_STATE_PASSED


AssertionException = include('AssertionException')


class AssertionRaising(AssertionBase):
    """
    Context manager, which checks for exception raise.
    
    Attributes
    ----------
    accept_subtypes : `bool`
        Whether subclasses are accepted as well.
    
    exception : `None | BaseException`
        Exception raised by the condition if any.
    
    expected_exceptions : `set<type<BaseException> | instance<BaseException>>`
        The expected exception types.
    
    received_exception : `None | BaseException`
        Exception raised within the context block if any.
    
    state : `int`
        The condition's state.
    
    where : `None | (BaseException) -> bool`
        Additional check to check the raised exception.
    
    Examples
    --------
    ```py
    with AssertionRaising(TypeError):
        'nice' + 69
    
    with AssertionRaising(ValueError(1)):
        raise ValueError(1)
    
    with AssertionRaising(ValueError, where = lambda err: err.args == (1,)):
        raise ValueError(1)
    ```
    """
    __slots__ = ('accept_subtypes', 'expected_exceptions', 'received_exception', 'where')
    
    def __new__(cls, expected_exception, *expected_exceptions, accept_subtypes = True, where = None):
        """
        Creates a new raise asserting context manager.
        
        Parameters
        ----------
        expected_exception : `type<BaseException> | instance<BaseException>˙
            The expected exception to be raised.
        
        *expected_exceptions : ˙tuple<type<BaseException> | instance<BaseException>>˙
            Additional expected exceptions.
        
        accept_subtypes : `bool` = `True`, Optional (Keyword only)
            Whether subclasses are accepted as well.
        
        where : `None | (BaseException) -> bool` = `None`, Optional (Keyword only)
            Additional check to check the raised exception.
        
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
        self.accept_subtypes = accept_subtypes
        self.expected_exceptions = expected_exceptions
        self.received_exception = None
        self.where = where
        
        return self
    
    
    @copy_docs(AssertionBase._build_repr_parts_into)
    def _build_repr_parts_into(self, into):
        into = AssertionBase._build_repr_parts_into(self, into)
        
        received_exception = self.received_exception
        if (received_exception is not None):
            into.append(', received_exception = ')
            into.append(repr(received_exception))
        
        return into
    
    
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
        
        self.received_exception = exception_value
        
        try:
            matched = try_match_exception(self.expected_exceptions, exception_value, self.accept_subtypes, self.where)
        except (SystemExit, KeyboardInterrupt):
            self.state = ASSERTION_STATE_FAILED
            raise
        
        except BaseException as exception:
            self.exception = exception
            matched = False
        
        if not matched:
            self.state = ASSERTION_STATE_FAILED
            try:
                raise AssertionException(self)
            finally:
                # Clear reference to self
                self = None
        
        self.state = ASSERTION_STATE_PASSED
        return True
