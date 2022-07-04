__all__ = ('get_function_environment_identifier',)

from .constants import (
    ENVIRONMENT_TYPE_COROUTINE, ENVIRONMENT_TYPE_COROUTINE_GENERATOR, ENVIRONMENT_TYPE_DEFAULT,
    ENVIRONMENT_TYPE_GENERATOR
)
from scarletio import is_coroutine_function,is_coroutine_generator_function, is_generator_function


def get_function_environment_identifier(func):
    """
    Gets the environment type depending on the given function's type.
    
    Parameters
    ----------
    func : `callable`
        The function to check.
    
    Returns
    -------
    identifier : `int`
    """
    if is_coroutine_generator_function(func):
        return ENVIRONMENT_TYPE_COROUTINE_GENERATOR
    
    if is_coroutine_function(func):
        return ENVIRONMENT_TYPE_COROUTINE
    
    if is_generator_function(func):
        return ENVIRONMENT_TYPE_GENERATOR
    
    return ENVIRONMENT_TYPE_DEFAULT
