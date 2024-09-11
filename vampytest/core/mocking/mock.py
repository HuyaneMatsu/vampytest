__all__ = ('mock_globals',)

from types import CodeType, FunctionType


BUILTINS = {
    name: __builtins__.get(name, NotImplemented) for name in (
        'ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError',
        'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError',
        'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis',
        'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError',
        'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError',
        'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError',
        'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError',
        'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError',
        'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration',
        'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError',
        'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError',
        'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError',
        '__import__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable',
        'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod',
        'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
        'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list',
        'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
        'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod',
        'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
    )
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


def _create_mocked_globals(potential_globals, recursion, old_globals, new_values):
    """
    Mocks the old globals dictionary returning the new ones.
    
    Parameters
    ----------
    potential_globals : `Generator`
        Generator over the potential globals we want to grab.
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
    
    # There is a python error I cannot reproduce with simple tests, but apparently some shit tries to access
    # `__builtins__` over actual globals
    try:
        builtins = old_globals['__builtins__']
    except KeyError:
        pass
    else:
        new_globals['__builtins__'] = builtins
    
    for name in potential_globals:
        try:
            value = old_globals[name]
        except KeyError:
            try:
                value = BUILTINS[name]
            except KeyError:
                # Variable missing ?!
                continue
        
        try:
            value = new_values[name]
        except KeyError:
            if recursion > 0:
                if isinstance(value, FunctionType):
                    value = _mock_function_globals(value, recursion, new_values)
        
        new_globals[name] = value
    
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
        _create_mocked_globals(_iter_potential_globals_of(to_mock), recursion, to_mock.__globals__, new_values),
        to_mock.__name__,
        to_mock.__defaults__,
        to_mock.__closure__,
    )
    mocked.__kwdefaults__ = to_mock.__kwdefaults__
    return mocked


def _iter_potential_globals_of(function):
    """
    Iterates over the potential globals of the given function.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    function : ``FunctionType`
        The function to check.
    
    Yields
    ------
    name : `str`
    """
    yielded = set()
    yielded_length = 0
    
    code_objects = _collect_code_objects(function)
    
    for code_object in code_objects:
        local_variable_names = {*code_object.co_varnames}
        for name in code_object.co_names:
            if name in local_variable_names:
                continue
            
            yielded.add(name)
            yielded_length_new = len(yielded)
            if yielded_length == yielded_length_new:
                continue
            
            yielded_length = yielded_length_new
            yield name
            continue


def _collect_code_objects(function):
    """
    Collects all the code objects present in the given function.
    
    Parameters
    ----------
    function : `FunctionType`
        The function to collect its code objects of.
    
    Returns
    -------
    code_objects : `set<CodeType>`
    """
    code_objects = set()
    to_do = [function.__code__]
    
    while to_do:
        code_object = to_do.pop()
        if code_object in code_objects:
            continue
        
        code_objects.add(code_object)
        
        constants = code_object.co_consts
        if constants is None:
            continue
        
        for constant in constants:
            if type(constant) is CodeType:
                to_do.append(constant)
    
    return code_objects
