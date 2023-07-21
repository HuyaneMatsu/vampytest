__all__ = ('mock_globals',)

from types import FunctionType


BUILTINS = {
    'ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError',
    'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError',
    'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError',
    'Exception', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning',
    'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError',
    'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError',
    'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
    'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError',
    'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError',
    'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError',
    'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning',
    'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', '__import__', 'abs', 'all', 'any', 'ascii', 'bin',
    'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright',
    'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format',
    'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance',
    'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object',
    'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
    'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
}


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
    
    # Add old values that are not present in the mocked ones
    for key, value in old_globals.items():
        if (key not in new_values):
            if recursion > 0:
                if isinstance(value, FunctionType):
                    value = _mock_function_globals(value, recursion, new_values)
        
            new_globals[key] = value
    
    # Mock values as required. We check them from both globals & builtins
    for key, value in new_values.items():
        if (key in old_globals.keys()) or (key in BUILTINS):
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
    mocked = FunctionType(
        to_mock.__code__,
        _mock_globals_dict(recursion, to_mock.__globals__, new_values),
        to_mock.__name__,
        to_mock.__defaults__,
        to_mock.__closure__,
    )
    mocked.__kwdefaults__ = to_mock.__kwdefaults__
    return mocked
