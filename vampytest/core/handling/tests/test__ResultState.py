from ...assertions import (
    assert_eq, assert_false, assert_in, assert_instance, assert_is, assert_is_not, assert_ne, assert_not_in,
    assert_true
)
from ...utils import _
from ...wrappers import call_from, call_with, raising

from ..result_state import RESULT_STATE_MODE_NONE, ResultState


def _assert_fields_set(result_state):
    """
    Asserts whether every fields are set of the given ``ResultState`` instance.
    
    Parameters
    ----------
    result_state : ``ResultState``
        The call state to check.
    """
    assert_instance(result_state, ResultState)
    assert_instance(result_state.mode, int)
    assert_instance(result_state.result, object, nullable = True)


def test__ResultState__new__empty():
    """
    Tests whether ``EmptyState.__new__`` works as intended.
    
    Case: No fields given.
    """
    result_state = ResultState()
    _assert_fields_set(result_state)
    
    assert_eq(result_state.mode, RESULT_STATE_MODE_NONE)
    assert_is(result_state.result, None)


def test__ResultState__repr__clean():
    """
    Tests whether ``ResultState.__repr__`` works as intended.
    
    Case: Clean.
    """
    result_state = ResultState()
    
    output = repr(result_state)
    
    assert_instance(output, str)
    assert_in(result_state.__class__.__name__, output)
    assert_not_in('returned_value = ', output)
    assert_not_in('raised_exception = ', output)


def test__ResultState__repr__return():
    """
    Tests whether ``ResultState.__repr__`` works as intended.
    
    Case: with return.
    """
    result_state = ResultState().with_return('koishi')
    
    output = repr(result_state)
    
    assert_instance(output, str)
    assert_in(result_state.__class__.__name__, output)
    assert_in('returned_value = ', output)
    assert_not_in('raised_exception = ', output)


def test__ResultState__repr__raise():
    """
    Tests whether ``ResultState.__repr__`` works as intended.
    
    Case: with raise.
    """
    result_state = ResultState().with_raise(BaseException('koishi'))
    
    output = repr(result_state)
    
    assert_instance(output, str)
    assert_in(result_state.__class__.__name__, output)
    assert_not_in('returned_value = ', output)
    assert_in('raised_exception = ', output)


def test__ResultState__eq():
    """
    Tests whether ``ResultState.__eq__`` works as intended.
    """
    result_state = ResultState()
    
    assert_eq(result_state, result_state)
    assert_ne(result_state, object())
    
    assert_ne(result_state, ResultState().with_return('koishi'))
    assert_ne(result_state, ResultState().with_raise(BaseException('koishi')))
    
    result_state = ResultState().with_return('koishi')
    assert_eq(result_state, result_state)


def _iter_options__bool():
    yield ResultState(), False
    yield ResultState().with_return('koishi'), True
    yield ResultState().with_raise(BaseException('koishi')), True


@_(call_from(_iter_options__bool()).returning_last())
def test__ResultState__bool(result_state):
    """
    Tests whether ``ResultState.__bool__`` works as intended.
    
    Parameters
    ----------
    result_state : ``ResultState``
        The result state to check.
    
    Returns
    -------
    output : `bool`
    """
    return bool(result_state)


def test__ResultState__copy__no_fields():
    """
    Tests whether ``ResultState.copy`` works as intended.
    
    Case: call state without fields.
    """
    result_state = ResultState()
    
    copy = result_state.copy()
    
    _assert_fields_set(copy)
    assert_is_not(result_state, copy)
    assert_eq(result_state, copy)


def test__ResultState__copy__all_fields():
    """
    Tests whether ``ResultState.copy`` works as intended.
    
    Case: Result state with all fields.
    """
    result_state = ResultState().with_return('koishi')
    
    copy = result_state.copy()
    
    _assert_fields_set(copy)
    assert_is_not(result_state, copy)
    assert_eq(result_state, copy)


def test__ResultState__with_return():
    """
    Tests whether ``ResultState.with_return`` works as intended.
    """
    return_value = object()
    
    result_state = ResultState().with_return(return_value)
    
    _assert_fields_set(result_state)
    assert_is(result_state.result, return_value)
    
    assert_true(result_state.is_return())
    assert_false(result_state.is_raise())


def test__ResultState__with_raise():
    """
    Tests whether ``ResultState.with_raise`` works as intended.
    """
    return_value = BaseException('koishi')
    
    result_state = ResultState().with_raise(return_value)
    
    _assert_fields_set(result_state)
    assert_is(result_state.result, return_value)
    
    assert_false(result_state.is_return())
    assert_true(result_state.is_raise())


@raising(TypeError)
@call_with(None)
@call_with(object())
def test__ResultState__with_raise__type_error(input_value):
    """
    Tests whether ``ResultState.with_raise`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass.
    
    Raises
    ------
    TypeError
    """
    ResultState().with_raise(input_value)


def _iter_options__is_return():
    yield ResultState(), False
    yield ResultState().with_return('koishi'), True
    yield ResultState().with_raise(BaseException('koishi')), False


@_(call_from(_iter_options__is_return()).returning_last())
def test__ResultState__is_return(call_state):
    """
    Tests whether ``ResultState.is_return`` works as intended.
    
    Parameters
    ----------
    result_state : ``ResultState``
        The result state to check.
    
    Returns
    -------
    output : `bool`
    """
    output = call_state.is_return()
    assert_instance(output, bool)
    return output


def _iter_options__is_raise():
    yield ResultState(), False
    yield ResultState().with_return('koishi'), False
    yield ResultState().with_raise(BaseException('koishi')), True


@_(call_from(_iter_options__is_raise()).returning_last())
def test__ResultState__is_raise(call_state):
    """
    Tests whether ``ResultState.is_raise`` works as intended.
    
    Parameters
    ----------
    result_state : ``ResultState``
        The result state to check.
    
    Returns
    -------
    output : `bool`
    """
    output = call_state.is_raise()
    assert_instance(output, bool)
    return output
