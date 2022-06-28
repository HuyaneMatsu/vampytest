__all__ = ()

def un_nest_expected_exceptions(exceptions):
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
    return set(iter_un_nest_expected_exceptions(exceptions))


def iter_un_nest_expected_exceptions(exceptions):
    """
    Called by ``un_nest_expected_exceptions`` or by itself to unwrap the exceptions.
    
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
            yield from iter_un_nest_expected_exceptions(exception)
        
        return
    
    if (
        (
            isinstance(exceptions, type) and
            issubclass(exceptions, BaseException)
        ) or
        isinstance(exceptions, BaseException)
    ):
        yield exceptions
        return
    
    raise TypeError(
        f'`exceptions` can be `tuple` of (`BaseException`, ...)`, got {exceptions.__class__.__name__}; {exceptions!r}.'
    )


def hash_object(object_):
    """
    Returns the hash value of the given object even if it not defines `__hash__`.
    
    Parameters
    ----------
    object_ : `Any`
        The object to get it's hash value of.
    
    Returns
    -------
    hash_value : `int`
    """
    try:
        hash_value = hash(object_)
    except (TypeError, NotImplementedError):
        hash_value = object.__hash__(object_)
    
    return hash_value


def try_hash_method(object_):
    """
    Tries different hash methods on the given object based on it's type.
    
    Parameters
    ----------
    object_ : `Any`
        The object to get it's hash value of.
    
    Returns
    -------
    hash_value : `int`
    """
    if isinstance(object_, tuple):
        return hash_tuple(object_)
    
    if isinstance(object_, list):
        return hash_list(object_)
    
    if isinstance(object_, dict):
        return hash_dict(object_)
    
    if isinstance(object_, set):
        return hash_set(object_)
    
    return hash_object(object_)


def hash_tuple(tuple_):
    """
    Returns the hash value of the given tuple.
    
    Parameters
    ----------
    tuple_ : `tuple` of `Any`
        The tuple to hash.
    
    Returns
    -------
    hash_value : `int`
    """
    hash_value = len(tuple_) << 4
    for element in tuple_:
        hash_value ^= try_hash_method(element)
    
    return hash_value


def hash_list(list_):
    """
    Returns the hash value of the given list.
    
    Parameters
    ----------
    list_ : `list` of `Any`
        The list to hash.
    
    Returns
    -------
    hash_value : `int`
    """
    hash_value = len(list_) << 8
    for element in list_:
        hash_value ^= try_hash_method(element)
    
    return hash_value


def hash_dict(dict_):
    """
    Returns the hash value of the given dict.
    
    Parameters
    ----------
    dict_ : `dict` of `Any`
        The dict to hash.
    
    Returns
    -------
    hash_value : `int`
    """
    hash_value = len(dict_) << 12
    
    for key, value in dict_.items():
        hash_value ^= try_hash_method(key) & try_hash_method(value)
    
    return hash_value


def hash_set(set_):
    """
    Returns the hash value of the given set.
    
    Parameters
    ----------
    set_ : `set` of `Any`
        The set to hash.
    
    Returns
    -------
    hash_value : `int`
    """
    hash_value = len(set_) << 16
    for element in set_:
        hash_value ^= try_hash_method(element)
    
    return hash_value


def maybe_merge_iterables(iterable_1, iterable_2):
    """
    Merges the two maybe iterable if applicable returning a new one.
    
    Parameters
    ----------
    iterable_1 : `None`, `iterable`
        Iterable to merge.
    iterable_2 : `None`, `iterable`
        Iterable to merge.
    
    Returns
    -------
    merged : `None`, `list`
    """
    if (iterable_1 is not None) and (not iterable_1):
        iterable_1 = None
    
    if (iterable_2 is not None) and (not iterable_2):
        iterable_2 = None
    
    if iterable_1 is None:
        if iterable_2 is None:
            merged = None
        else:
            merged = [*iterable_2]
    else:
        if iterable_2 is None:
            merged = [*iterable_1]
        else:
            merged = [*iterable_1, *iterable_2]
    
    return merged


def maybe_merge_mappings(mapping_1, mapping_2):
    """
    Merges the two maybe mapping if applicable returning a new one.
    
    Parameters
    ----------
    mapping_1 : `None`, `mapping`
        Mapping to merge.
    mapping_2 : `None`, `mapping`
        Mapping to merge.
    
    Returns
    -------
    merged : `None`, `dict`
    """
    if (mapping_1 is not None) and (not mapping_1):
        mapping_1 = None
    
    if (mapping_2 is not None) and (not mapping_2):
        mapping_2 = None
    
    if mapping_1 is None:
        if mapping_2 is None:
            merged = None
        else:
            merged = {**mapping_2}
    else:
        if mapping_2 is None:
            merged = {**mapping_1}
        else:
            merged = {**mapping_1, **mapping_2}
    
    return merged


def try_match_exception(expected_exceptions, received_exception, accept_subtypes):
    """
    Checks whether the received exception matches the preset ones.
    
    Parameters
    ----------
    expected_exceptions : `set` of `BaseException`
        The expected exceptions.
    received_exception : `BaseException`
        The received exception.
    accept_subtypes : `bool`
        Whether sub classes are allowed.
    
    Returns
    -------
    exception_matched : `bool`
    """
    for expected_exception in expected_exceptions:
        if isinstance(expected_exception, type):
            exception_type = expected_exception
            exception_value = None
        
        else:
            exception_type = type(expected_exception)
            exception_value = expected_exception
        
        
        if accept_subtypes:
            if not isinstance(received_exception, exception_type):
                continue
        
        else:
            if type(received_exception) is not exception_type:
                continue
        
        if (exception_value is not None) and (exception_value.args != received_exception.args):
            continue
        
        exception_matched = True
        break
    
    else:
        exception_matched = False
    
    return exception_matched
