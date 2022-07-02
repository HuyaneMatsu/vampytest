__all__ = ('get_function_environment_type',)

from .type_ import EnvironmentType

from scarletio import is_coroutine_function,is_coroutine_generator_function, is_generator_function


def get_function_environment_type(func):
    """
    Gets the environment type depending on the given function's type.
    
    Parameters
    ----------
    func : `callable`
        The function to check.
    
    Returns
    -------
    type_ : ``EnvironmentType``
    """
    if is_coroutine_generator_function(func):
        return EnvironmentType.coroutine_generator
    
    if is_coroutine_function(func):
        return EnvironmentType.coroutine
    
    if is_generator_function(func):
        return EnvironmentType.generator
    
    return EnvironmentType.default
