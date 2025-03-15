from ...assertions import assert_eq, assert_in, assert_instance, assert_is, assert_is_not, assert_not_in
from ...utils import _
from ...wrappers import call_from

from ..call_state import CallState


def _assert_fields_set(call_state):
    """
    Asserts whether every fields are set of the given ``CallState`` instance.
    
    Parameters
    ----------
    call_state : ``CallState``
        The call state to check.
    """
    assert_instance(call_state, CallState)
    assert_instance(call_state.keyword_parameters, dict, nullable = True)
    assert_instance(call_state.name, str, nullable = True)
    assert_instance(call_state.positional_parameters, list, nullable = True)


def test__CallState__new():
    """
    Tests whether ``CallState.__new__`` works as intended.
    """
    call_state = CallState()
    _assert_fields_set(call_state)
    
    assert_is(call_state.keyword_parameters, None)
    assert_is(call_state.positional_parameters, None)


def test__CallState__repr__clean():
    """
    Tests whether ``CallState.__repr__`` works as intended.
    
    Case: Clean.
    """
    call_state = CallState()
    
    output = repr(call_state)
    
    assert_instance(output, str)
    assert_in(type(call_state).__name__, output)
    assert_not_in('positional_parameters = ', output)
    assert_not_in('keyword_parameters = ', output)
    assert_not_in('name = ', output)


def test__CallState__repr__positional():
    """
    Tests whether ``CallState.__repr__`` works as intended.
    
    Case: with positional parameters.
    """
    call_state = CallState().with_parameters(['koishi'], None)
    
    output = repr(call_state)
    
    assert_instance(output, str)
    assert_in(type(call_state).__name__, output)
    assert_in('positional_parameters = ', output)
    assert_not_in('keyword_parameters = ', output)
    assert_not_in('name = ', output)


def test__CallState__repr__keyword():
    """
    Tests whether ``CallState.__repr__`` works as intended.
    
    Case: with keyword parameters.
    """
    call_state = CallState().with_parameters(None, {'satori': 'smug'})
    
    output = repr(call_state)
    
    assert_instance(output, str)
    assert_in(call_state.__class__.__name__, output)
    assert_not_in('positional_parameters = ', output)
    assert_in('keyword_parameters = ', output)
    assert_not_in('name = ', output)


def test__CallState__repr__positional_and_keyword():
    """
    Tests whether ``CallState.__repr__`` works as intended.
    
    Case: with both positional and keyword parameters.
    """
    call_state = CallState().with_parameters(['koishi'], {'satori': 'smug'})
    
    output = repr(call_state)
    
    assert_instance(output, str)
    assert_in(call_state.__class__.__name__, output)
    assert_in('positional_parameters = ', output)
    assert_in('keyword_parameters = ', output)
    assert_not_in('name = ', output)



def test__CallState__repr__named():
    """
    Tests whether ``CallState.__repr__`` works as intended.
    
    Case: with name.
    """
    call_state = CallState().with_name('orin')
    
    output = repr(call_state)
    
    assert_instance(output, str)
    assert_in(call_state.__class__.__name__, output)
    assert_not_in('positional_parameters = ', output)
    assert_not_in('keyword_parameters = ', output)
    assert_in('name = ', output)


def _iter_options__eq():
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        True,
    )
    
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        (
            (CallState.with_parameters, (None, {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        False,
    )
    
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        (
            (CallState.with_parameters, (['koishi'], None)),
            (CallState.with_name, ('orin',)),
        ),
        False,
    )
    
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('okuu',)),
        ),
        False,
    )
    
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        (
            (CallState.with_name, ('orin',)),
        ),
        False,
    )
    
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
        ),
        False,
    )
    
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
            (CallState.with_name, ('orin',)),
        ),
        None,
        False,
    )


@_(call_from(_iter_options__eq()).returning_last())
def test__CallState__eq(prepare_functions_and_parameters_0, prepare_functions_and_parameters_1):
    """
    Tests whether ``CallState.__eq__`` works as intended.
    
    Parameters
    ----------
    prepare_functions_and_parameters_0 : `None | tuple<(FunctionType, tuple<object>)>`
        Functions and parameters for the to prepare an instance for the test.
    
    prepare_functions_and_parameters_1 : `None | tuple<(FunctionType, tuple<object>)>`
        Functions and parameters for the to prepare an instance for the test.
    
    Returns
    -------
    output : `bool`
    """
    call_state_0 = CallState()
    if (prepare_functions_and_parameters_0 is not None):
        for prepare_function, parameters in prepare_functions_and_parameters_0:
            call_state_0 = prepare_function(call_state_0, *parameters)
    
    call_state_1 = CallState()
    if (prepare_functions_and_parameters_1 is not None):
        for prepare_function, parameters in prepare_functions_and_parameters_1:
            call_state_1 = prepare_function(call_state_1, *parameters)
    
    output = call_state_0 == call_state_1
    assert_instance(output, bool)
    return output


def test__CallState__hash():
    """
    Tests whether ``CallState.__hash__`` works as intended.
    """
    call_state = CallState().with_parameters(['koishi'], {'satori': 'smug'}).with_name('orin')
    
    assert_instance(hash(call_state), int)


def _iter_options__bool():
    yield (
        None,
        False,
    )
    
    yield (
        (
            (CallState.with_parameters, (['koishi'], None)),
        ),
        True,
    )
    
    yield (
        (
            (CallState.with_parameters, (None, {'satori': 'smug'})),
        ),
        True,
    )
    
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
        ),
        True,
    )
    
    yield (
        (
            (CallState.with_name, ('orin',)),
        ),
        True,
    )


@_(call_from(_iter_options__bool()).returning_last())
def test__CallState__bool(prepare_functions_and_parameters):
    """
    Tests whether ``CallState.__bool__`` works as intended.
    
    Parameters
    ----------
    prepare_functions_and_parameters : `None | tuple<(FunctionType, tuple<object>)>`
        Functions and parameters for the to prepare an instance for the test.
    
    Returns
    -------
    output : `bool`
    """
    call_state = CallState()
    if (prepare_functions_and_parameters is not None):
        for prepare_function, parameters in prepare_functions_and_parameters:
            call_state = prepare_function(call_state, *parameters)
    
    return bool(call_state)


def test__CallState__copy__no_fields():
    """
    Tests whether ``CallState.copy`` works as intended.
    
    Case: call state without fields.
    """
    call_state = CallState()
    
    copy = call_state.copy()
    
    _assert_fields_set(copy)
    assert_is_not(call_state, copy)
    assert_eq(call_state, copy)


def test__CallState__copy__all_fields():
    """
    Tests whether ``CallState.copy`` works as intended.
    
    Case: Call state with all fields.
    """
    call_state = CallState().with_parameters(['koishi'], {'satori': 'smug'})
    
    copy = call_state.copy()
    
    _assert_fields_set(copy)
    assert_is_not(call_state, copy)
    assert_eq(call_state, copy)


def _iter_options__with_parameters():
    # Nothing
    yield (
        None,
        (
            (CallState.with_parameters, (None, None)),
        ),
        (
            None,
            None,
            None,
        )
    )
    
    # empty list
    yield (
        None,
        (
            (CallState.with_parameters, ([], None)),
        ),
        (
            None,
            None,
            None,
        )
    )
    
    # empty dict
    yield (
        None,
        (
            (CallState.with_parameters, (None, {})),
        ),
        (
            None,
            None,
            None,
        )
    )
    
    # Add list
    yield (
        None,
        (
            (CallState.with_parameters, (['koishi', 'orin'], None)),
        ),
        (
            ['koishi', 'orin'],
            None,
            None,
        )
    )
    
    # Add dict
    yield (
        None,
        (
            (CallState.with_parameters, (None, {'satori': 'smug', 'okuu': 'unyu'})),
        ),
        (
            None,
            {'satori': 'smug', 'okuu': 'unyu'},
            None,
        )
    )
    
    # Extend list
    yield (
        (
            (CallState.with_parameters, (['koishi'], None)),
        ),
        (
            (CallState.with_parameters, (['orin'], None)),
        ),
        (
            ['koishi', 'orin'],
            None,
            None,
        )
    )
    
    # Extend dict
    yield (
        (
            (CallState.with_parameters, (None, {'satori': 'smug'})),
        ),
        (
            (CallState.with_parameters, (None, {'okuu': 'unyu'})),
        ),
        (
            None,
            {'satori': 'smug', 'okuu': 'unyu'},
            None,
        )
    )
    
    # Duplicate list
    yield (
        (
            (CallState.with_parameters, (['koishi'], None)),
        ),
        (
            (CallState.with_parameters, (['koishi'], None)),
        ),
        (
            ['koishi', 'koishi'],
            None,
            None,
        )
    )
    
    # Duplicate dict
    yield (
        (
            (CallState.with_parameters, (None, {'satori': 'smug'})),
        ),
        (
            (CallState.with_parameters, (None, {'satori': 'unyu'})),
        ),
        (
            None,
            {'satori': 'unyu'},
            None,
        )
    )
    
    # Keep name
    yield (
        (
            (CallState.with_name, ('orin',)),
        ),
        (
            (CallState.with_parameters, (None, None)),
        ),
        (
            None,
            None,
            'orin',
        )
    )
    
    # Keep values
    yield (
        (
            (CallState.with_parameters, (['koishi'], {'satori': 'smug'})),
        ),
        (
            (CallState.with_name, ('orin',)),
        ),
        (
            ['koishi'],
            {'satori': 'smug'},
            'orin',
        )
    )


@_(call_from(_iter_options__with_parameters()).returning_last())
def test__CallState__with_functions(prepare_functions_and_parameters, action_functions_and_parameters):
    """
    Tests whether ``CallState.with_parameters`` works as intended.
    
    Parameters
    ----------
    prepare_functions_and_parameters : `None | tuple<(FunctionType, tuple<object>)>`
        Functions and parameters for the to prepare an instance for the test.
    
    action_functions_and_parameters : `None | tuple<(FunctionType, tuple<object>)>`
        Functions and parameters to execute on instance for the test.
    
    Returns
    -------
    output : ``CallState``
    """
    call_state = CallState()
    if (prepare_functions_and_parameters is not None):
        for prepare_function, parameters in prepare_functions_and_parameters:
            call_state = prepare_function(call_state, *parameters)
    
    output_call_state = call_state
    for prepare_function, parameters in action_functions_and_parameters:
        output_call_state = prepare_function(output_call_state, *parameters)
    
    _assert_fields_set(call_state)
    assert_is_not(call_state, output_call_state)
    
    return (
        output_call_state.positional_parameters,
        output_call_state.keyword_parameters,
        output_call_state.name,
    )
