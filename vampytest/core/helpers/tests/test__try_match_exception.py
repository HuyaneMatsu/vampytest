from vampytest import _, call_with

from ..exception_matching import try_match_exception


@_(call_with({IndexError}, IndexError(), True).returning(True))
@_(call_with({IndexError}, IndexError(), False).returning(True))
@_(call_with({IndexError()}, IndexError(), True).returning(True))
@_(call_with({IndexError()}, IndexError(), False).returning(True))
@_(call_with({IndexError(0)}, IndexError(0), True).returning(True))
@_(call_with({IndexError(0)}, IndexError(1), True).returning(False))
@_(call_with({LookupError}, IndexError(), True).returning(True))
@_(call_with({LookupError}, IndexError(), False).returning(False))
@_(call_with({LookupError()}, IndexError(), True).returning(True))
@_(call_with({LookupError()}, IndexError(), False).returning(False))
@_(call_with({LookupError(0)}, IndexError(0), True).returning(True))
@_(call_with({LookupError(0)}, IndexError(0), False).returning(False))
@_(call_with({LookupError(0)}, IndexError(1), True).returning(False))
def test_try_match_exception(expected_exceptions, received_exception, accept_subtypes):
    return try_match_exception(expected_exceptions, received_exception, accept_subtypes)
