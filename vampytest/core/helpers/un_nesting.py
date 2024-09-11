__all__ = ()


def un_nest(value):
    """
    Un-nests the given value into a tuple.
    
    Parameters
    ----------
    value : `tuple<object>`, `object`
        The value to un-nest.
    
    Returns
    -------
    value : `tuple<object>`
    """
    return {*iter_un_nest(value)}


def iter_un_nest(value):
    """
    Un-nests the given tuple.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    value : `tuple<object>`, `object`
        The value to un-nest.
    
    Yields
    ------
    value : `object`
    """
    to_do = [value]
    
    while to_do:
        value = to_do.pop()
        if isinstance(value, tuple):
            to_do.extend(value)
            continue
        
        yield value
        continue


def un_nest_exceptions(exceptions):
    """
    Un-nests the given `exceptions`.
    
    Parameters
    ----------
    exceptions : `BaseException | type<BaseException> | tuple<BaseException, <type<BaseException>, ...>`
        The exceptions to un-nest.
    
    Returns
    -------
    exceptions : `set` of (`BaseException`, `type<BaseException>`)
    
    Raises
    ------
    TypeError
        If an element's type is incorrect.
    """
    exceptions = un_nest(exceptions)
    
    for exception in exceptions:
        if isinstance(exception, BaseException):
            continue
        
        if isinstance(exception, type) and issubclass(exception, BaseException):
            continue
        
        raise TypeError(
            f'`exception` can be `BaseException` or its instance, `tuple` of (`BaseException`, ...)`, '
            f'got {exception.__class__.__name__}; {exception!r}.'
        )
    
    return exceptions


def un_nest_types(types):
    """
    Un-nests the given `types`.
    
    Parameters
    ----------
    types : `type<type> | tuple<type<type>, ...>`
        The types to un-nest.
    
    Returns
    -------
    types : `set` of `type`
    
    Raises
    ------
    TypeError
        If an element's type is incorrect.
    """
    types = un_nest(types)
    
    for type_value in types:
        if not isinstance(type_value, type):
            raise TypeError(
                f'`type` can be `type`, `tuple` of (`type`, ...)`, '
                f'got {type(type_value).__name__}; {type_value!r}.'
            )
    
    return types
