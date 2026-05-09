__all__ = ()


def try_match_exception(expected_exceptions, received_exception, accept_subtypes, where):
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
    where : `None`, `callable`
        Additional check to check the raised exception.
    
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
        
        if (where is not None) and (not where(received_exception)):
            continue
        
        exception_matched = True
        break
    
    else:
        exception_matched = False
    
    return exception_matched
