__all__ = ('_',)


def _(value):
    """
    Wraps nothing and returns the value.
    
    Since python does not allow using arbitrary expression in decorators, it can be used to wrap the expression.
    
    Parameters
    ----------
    value : `object`
        The value to return.
    
    Returns
    -------
    value : `value`
    """
    return value
