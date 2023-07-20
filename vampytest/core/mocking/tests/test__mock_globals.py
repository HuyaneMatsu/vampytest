from datetime import datetime as DateTime

from vampytest import assert_is, call_from

from ..mock import mock_globals


def b():
    out = DateTime.utcnow()
    assert_is(out, None)

def a():
    out = DateTime.utcnow()
    assert_is(out, None)
    
    b()


def _iter_options():
    class mocked_date_time:
        def utcnow():
            return None
    
    yield b, 0, {'DateTime': mocked_date_time}
    yield a, 2, {'DateTime': mocked_date_time}
    yield a, 1, {'DateTime': mocked_date_time, 'b': lambda: None}


@call_from(_iter_options())
def test__mock_globals(to_mock, recursion, values):
    mocked = mock_globals(to_mock, recursion, values)
    mocked()
