from vampytest import _, call_with

from ..exception_matching import try_match_exception


@_(call_with({IndexError}, IndexError(), True, None).returning(True))
@_(call_with({IndexError}, IndexError(), False, None).returning(True))
@_(call_with({IndexError()}, IndexError(), True, None).returning(True))
@_(call_with({IndexError()}, IndexError(), False, None).returning(True))
@_(call_with({IndexError(0)}, IndexError(0), True, None).returning(True))
@_(call_with({IndexError(0)}, IndexError(1), True, None).returning(False))
@_(call_with({LookupError}, IndexError(), True, None).returning(True))
@_(call_with({LookupError}, IndexError(), False, None).returning(False))
@_(call_with({LookupError()}, IndexError(), True, None).returning(True))
@_(call_with({LookupError()}, IndexError(), False, None).returning(False))
@_(call_with({LookupError(0)}, IndexError(0), True, None).returning(True))
@_(call_with({LookupError(0)}, IndexError(0), False, None).returning(False))
@_(call_with({LookupError(0)}, IndexError(1), True, None).returning(False))
@_(call_with({IndexError}, IndexError(1), True, lambda err: err.args == (1,)).returning(True))
@_(call_with({IndexError}, IndexError(2), True, lambda err: err.args == (1,)).returning(False))
def test_try_match_exception(expected_exceptions, received_exception, accept_subtypes, where):
    return try_match_exception(expected_exceptions, received_exception, accept_subtypes, where)
