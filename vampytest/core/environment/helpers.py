__all__ = ('get_function_environment_identifier', 'shutdown_environments',)

from scarletio import is_coroutine_function,is_coroutine_generator_function, is_generator_function

from .configuration import ENVIRONMENTS_BY_SCOPE
from .constants import (
    ENVIRONMENT_TYPE_COROUTINE, ENVIRONMENT_TYPE_COROUTINE_GENERATOR, ENVIRONMENT_TYPE_DEFAULT,
    ENVIRONMENT_TYPE_GENERATOR
)


def get_function_environment_identifier(func):
    """
    Gets the environment type depending on the given function's type.
    
    Parameters
    ----------
    func : `FunctionType`
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


def shutdown_environments():
    """
    Shuts down all the registered environments. This operation cannot be reversed.
    """
    for environment_by_detail in ENVIRONMENTS_BY_SCOPE.values():
        for environments_by_identifier in environment_by_detail.values():
            for environment in environments_by_identifier.values():
                environment.shutdown()
