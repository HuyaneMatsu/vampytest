from datetime import datetime as DateTime, timezone as TimeZone

from vampytest import assert_eq, assert_is, assert_true, call_from

from ..mock import mock_globals


def b():
    out = DateTime.now(TimeZone.utc)
    assert_is(out, None)


def a():
    out = DateTime.now(TimeZone.utc)
    assert_is(out, None)
    
    b()


def _iter_options():
    class mocked_date_time:
        def now(time_zone):
            return None
    
    yield b, 0, {'DateTime': mocked_date_time}
    yield a, 2, {'DateTime': mocked_date_time}
    yield a, 1, {'DateTime': mocked_date_time, 'b': lambda: None}


@call_from(_iter_options())
def test__mock_globals(to_mock, recursion, values):
    """
    Tests whether ``mock_globals`` works as intended.
    
    Parameters
    ----------
    to_mock : `FunctionType`
        The function to mock.
    recursion : `int`
        Recursion level.
    values : `dict<str, object>`
        The values to mock.
    """
    mocked = mock_globals(to_mock, recursion, values)
    mocked()


def test__mock_globals__keyword_default_not_lost():
    """
    Tests whether keyword defaults aren ot lost when using ``mock_globals``.
    """
    sentinel = object()
    
    def c(*, parameter_0 = sentinel):
        return parameter_0
    
    mocked = mock_globals(c)
    
    output = mocked()
    assert_is(output, sentinel)


def d():
    return isinstance(1, bool)


def test__mock_globals__builtins():
    """
    Tests whether builtins are mocked when using ``mock_globals``.
    """
    mocked = mock_globals(d, isinstance = lambda x, y: True)
    
    output = mocked()
    
    assert_true(output)


def test__mock_globals__builtins__no_error():
    """
    Tests whether builtins are still working after ``mock_globals`` call.
    """
    mocked = mock_globals(d)
    
    # We dont care about the output
    mocked()


def f(value):
    return 1


def e():
    return [f(value) for value in range(2)]


def test__mock_globals__inline_generator_no_fail():
    """
    Tests whether ``mock_globals`` works as intended.
    
    Case: handling inline generators & do not fail.
    """
    mocked = mock_globals(e)
    
    # We dont care about the output
    mocked()


def test__mock_globals__inline_generator_mock_nested():
    """
    Tests whether ``mock_globals`` works as intended.
    
    Case: handling inline generators & mock nested.
    """
    mocked = mock_globals(e, f = (lambda value: 2))
    
    output = mocked()
    assert_eq(output, [2, 2])
