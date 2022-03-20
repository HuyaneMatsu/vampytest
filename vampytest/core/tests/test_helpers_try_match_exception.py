from ..helpers import try_match_exception

from vampytest import call_with

test_try_match_exception = (
    try_match_exception
    @call_with({IndexError}, IndexError(), True).returning(True)
    @call_with({IndexError}, IndexError(), False).returning(True)
    @call_with({IndexError()}, IndexError(), True).returning(True)
    @call_with({IndexError()}, IndexError(), False).returning(True)
    @call_with({IndexError(0)}, IndexError(0), True).returning(True)
    @call_with({IndexError(0)}, IndexError(1), True).returning(False)
    @call_with({LookupError}, IndexError(), True).returning(True)
    @call_with({LookupError}, IndexError(), False).returning(False)
    @call_with({LookupError()}, IndexError(), True).returning(True)
    @call_with({LookupError()}, IndexError(), False).returning(False)
    @call_with({LookupError(0)}, IndexError(0), True).returning(True)
    @call_with({LookupError(0)}, IndexError(0), False).returning(False)
    @call_with({LookupError(0)}, IndexError(1), True).returning(False)
)
