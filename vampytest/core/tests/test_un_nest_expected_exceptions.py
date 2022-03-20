from ..helpers import un_nest_expected_exceptions

from vampytest import call_with

test_un_nest_expected_exceptions = (
    un_nest_expected_exceptions
    @call_with((IndexError,)).returning({IndexError})
    @call_with((IndexError, IndexError)).returning({IndexError})
    @call_with((IndexError(1),)).returning_transformed(set)
    @call_with((IndexError(1), ValueError)).returning_transformed(set)
    @call_with((6,)).raising(TypeError)
)
