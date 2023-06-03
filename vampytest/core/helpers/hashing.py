__all__ = ()


def hash_object(object_):
    """
    Returns the hash value of the given object even if it not defines `__hash__`.
    
    Parameters
    ----------
    object_ : `object`
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
    object_ : `object`
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
    tuple_ : `tuple` of `object`
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
    list_ : `list` of `object`
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
    dict_ : `dict` of `object`
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
    set_ : `set` of `object`
        The set to hash.
    
    Returns
    -------
    hash_value : `int`
    """
    hash_value = len(set_) << 16
    for element in set_:
        hash_value ^= try_hash_method(element)
    
    return hash_value
