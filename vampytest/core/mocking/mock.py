__all__ = ('mock_globals',)

from types import FunctionType


def mock_globals(to_mock, recursion = -1, values = None, **keyword_parameters):
    """
    Mocks the globals of the given function.
    
    Parameters
    ----------
    to_mock : `FunctionType`
        The function to mock.
    recursion : `int` = `-1`, Optional
        Recursion level. Can be used to mock nested function if given as `> 1`.
    values : `None | dict<str, object>` = `None`, Optional
        Can be used to define the values to mock from a dictionary.
    **keyword_parameters : `dict<str, object>`
        Additional keyword values to define values as mock easier if their name is not an overlap with an actual
        parameter.
    
    Returns
    -------
    mocked : `instance<type<to_mock>>`
        The mocked function.
    """
    if values is not None:
        keyword_parameters.update(values)
    
    if isinstance(to_mock, FunctionType):
        return _mock_function_globals(to_mock, recursion, keyword_parameters)
    
    raise TypeError(
        f'Cannot mock {to_mock.__class__.__name__}; {to_mock!r}.'
    )


def _mock_globals_dict(recursion, old_globals, new_values):
    """
    Mocks the old globals dictionary returning the new ones.
    
    Parameters
    ----------
    recursion : `int`
        Recursion level.
    old_globals : `dict<str, object>`
        The old globals to mock.
    new_values : `dict<str, object>`
        The new values to mock with.
    
    Returns
    -------
    mew_globals : `dict<str, object>`
    """
    new_globals = {}
    
    recursion -= 1
    
    for key, value in old_globals.items():
        try:
            value = new_values[key]
        except KeyError:
            if recursion > 0:
                if isinstance(value, FunctionType):
                    value = _mock_function_globals(value, recursion, new_values)
        
        new_globals[key] = value
    
    return new_globals


def _mock_function_globals(to_mock, recursion, new_values):
    """
    Mocks a function's globals.
    
    Parameters
    ----------
    to_mock : `FunctionType`
        The function to mock.
    recursion : `int`
        Recursion level.
    new_values : `dict<str, object>`
        The new values to mock with.
    
    Returns
    -------
    mocked : `FunctionType`
        The mocked function.
    """
    return FunctionType(
        to_mock.__code__,
        _mock_globals_dict(recursion, to_mock.__globals__, new_values),
        to_mock.__name__,
        to_mock.__defaults__,
        to_mock.__closure__,
    )
