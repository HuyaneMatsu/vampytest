__all__ = ('AssertionRaising', )

from . import assertion_states as CONDITION_STATES
from .assertion_base import AssertionBase
from .exceptions import AssertionException



def un_nest_exception_types(exceptions):
    """
    Un-wraps the given `exceptions` recursively.
    
    Parameters
    ----------
    exceptions : `tuple` of (`BaseException`, ...)
        The exceptions to unwrap.
    
    Returns
    -------
    exceptions : `set` of ``BaseException``
    
    Raises
    ------
    TypeError
        If an element's type is incorrect.
    """
    return set(iter_un_nest_exception_types(exceptions))


def iter_un_nest_exception_types(exceptions):
    """
    Called by ``un_nest_exception_types`` or by itself to unwrap the exceptions.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    exceptions : `tuple` of (`BaseException`, ...)
        The exceptions to unwrap.
    
    Yields
    ------
    exception : `BaseException`
    
    Raises
    ------
    TypeError
        If an element's type is incorrect.
    """
    if isinstance(exceptions, tuple):
        for exception in exceptions:
            yield from iter_un_nest_exception_types(exception)
    
    
    if issubclass(exceptions, BaseException):
        yield exceptions
    
    
    raise TypeError(
        f'`exceptions` can be `tuple` of (`BaseException`, ...)`, got {exceptions.__class__.__name__}; {exceptions!r}.'
    )


class AssertionRaising(AssertionBase):
    """
    Context manager, which checks for exception raise.
    
    Attributes
    ----------
    state : `str`
        The condition's state.
    exception : `None`, `BaseException`
        Exception raised by the condition if any.
    accept_sub_classes : `bool`
        Whether subclasses are accepted as well.
    exception_types : `set` of ``BaseException``
        The expected exception types.
    
    Examples
    --------
    ```py
    with AssertionRaising(TypeError):
        'nice' + 69
    ```
    """
    __slots__ = ('accept_sub_classes', 'exception', 'exception_types')
    
    def __new__(cls, *exception_types, accept_sub_classes=True):
        """
        Creates a new raise asserting context manager.
        
        Parameters
        ----------
        *exception_types : tuple` of (`BaseException`, ...)
            Exception types to expect.
        accept_sub_classes : `bool` = `True`
            Whether subclasses are accepted as well.
        
        Raises
        ------
        TypeError
            If an `exception_types`'s type is incorrect.
        ValueError
            If no exception was passed.
        """
        exception_types = un_nest_exception_types(exception_types)
        if not exception_types:
            raise ValueError('At least 1 exception is required.')
        
        self = AssertionBase.__new__(cls)
        self.exception_types = exception_types
        
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
        
        if self.accept_sub_classes:
            for exception_type in self.exception_types:
                if issubclass(exc_type, exception_type):
                    exception_type_correct = True
                    break
            else:
                exception_type_correct = False
        
        else:
            exception_type_correct = (exc_type in self.exception_types)
        
        
        if exception_type_correct:
            self.state = CONDITION_STATES.PASSED
            return True
        
        self.state = CONDITION_STATES.FAILED
        return False
