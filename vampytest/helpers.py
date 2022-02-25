__all__ = ()

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
