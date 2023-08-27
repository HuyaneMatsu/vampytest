from ...assertions import assert_eq, assert_in, assert_instance, assert_is, assert_is_not, assert_ne, assert_not_in
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
    assert_in(call_state.__class__.__name__, output)
    assert_not_in('positional_parameters = ', output)
    assert_not_in('keyword_parameters = ', output)


def test__CallState__repr__positional():
    """
    Tests whether ``CallState.__repr__`` works as intended.
    
    Case: with positional parameters.
    """
    call_state = CallState().with_parameters(['koishi'], None)
    
    output = repr(call_state)
    
    assert_instance(output, str)
    assert_in(call_state.__class__.__name__, output)
    assert_in('positional_parameters = ', output)
    assert_not_in('keyword_parameters = ', output)


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


def test__CallState__repr__both():
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


def test__CallState__eq():
    """
    Tests whether ``CallState.__eq__`` works as intended.
    """
    call_state = CallState().with_parameters(['koishi'], {'satori': 'smug'})
    
    assert_eq(call_state, call_state)
    assert_ne(call_state, object())
    
    for with_parameters in (
        (None, None), (['koishi'], None), (None, {'satori': 'smug'}), (['orin'], {'satori': 'smug'}),
        (['koishi'], {'okuu': 'smug'}), (['koishi'], {'satori': 'parsee'}),):
        test_call_state = CallState().with_parameters(*with_parameters)
        assert_ne(test_call_state, call_state)


def test__CallState__hash():
    """
    Tests whether ``CallState.__hash__`` works as intended.
    """
    call_state = CallState().with_parameters(['koishi'], {'satori': 'smug'})
    
    assert_instance(hash(call_state), int)


def _iter_options__bool():
    yield CallState(), False
    yield CallState().with_parameters(['koishi'], None), True
    yield CallState().with_parameters(None, {'satori': 'smug'}), True
    yield CallState().with_parameters(['koishi'], {'satori': 'smug'}), True


@_(call_from(_iter_options__bool()).returning_last())
def test__CallState__bool(call_state):
    """
    Tests whether ``CallState.__bool__`` works as intended.
    
    Parameters
    ----------
    call_state : ``CallState``
        The call state to gets its truth value of.
    
    Returns
    -------
    output : `bool`
    """
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
    call_state_out = CallState()
    yield CallState(), None, None, call_state_out
    
    # Empty
    call_state_out = CallState()
    yield CallState(), [], None, call_state_out
    
    call_state_out = CallState()
    yield CallState(), None, {}, call_state_out
    
    # Add (multiple, no need for simple)
    call_state_out = CallState()
    call_state_out.positional_parameters = ['koishi', 'orin']
    yield CallState(), ['koishi', 'orin'], None, call_state_out
    
    call_state_out = CallState()
    call_state_out.keyword_parameters = {'satori': 'smug', 'okuu': 'unyu'}
    yield CallState(), None, {'satori': 'smug', 'okuu': 'unyu'}, call_state_out
    
    # Extend
    call_state_out = CallState()
    call_state_out.positional_parameters = ['koishi', 'orin']
    yield CallState().with_parameters(['koishi'], None), ['orin'], None, call_state_out
    
    call_state_out = CallState()
    call_state_out.keyword_parameters = {'satori': 'smug', 'okuu': 'unyu'}
    yield CallState().with_parameters(None, {'satori': 'smug'}), None, {'okuu': 'unyu'}, call_state_out
    
    # Duplicates
    call_state_out = CallState()
    call_state_out.positional_parameters = ['koishi', 'koishi']
    yield CallState().with_parameters(['koishi'], None), ['koishi'], None, call_state_out
    
    call_state_out = CallState()
    call_state_out.keyword_parameters = {'satori': 'unyu'}
    yield CallState().with_parameters(None, {'satori': 'smug'}), None, {'satori': 'unyu'}, call_state_out


@_(call_from(_iter_options__with_parameters()).returning_last())
def test__CallState__with_parameters(call_state, positional_parameters, keyword_parameters):
    """
    Tests whether ``CallState.with_parameters`` works as intended.
    
    Parameters
    ----------
    call_state : ``CallState``
        The call state to extend.
    positional_parameters : `None`, `list` of `object`
        Positional parameters to the the test function with.
    keyword_parameters : `None`, `dict` of (`str`, `object`) items
        Keyword parameters to the call the test function with.
    
    Returns
    -------
    output : ``CallState``
    """
    output = call_state.with_parameters(positional_parameters, keyword_parameters)
    
    _assert_fields_set(output)
    assert_is_not(call_state, output)
    
    return output
