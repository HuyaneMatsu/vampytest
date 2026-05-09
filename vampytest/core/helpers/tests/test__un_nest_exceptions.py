from vampytest import _, call_with

from ..un_nesting import un_nest_exceptions


@_(call_with(IndexError).returning({IndexError}))
@_(call_with((IndexError,)).returning({IndexError}))
@_(call_with((IndexError(1),)).returning_transformed(set))
@_(call_with((IndexError, IndexError)).returning({IndexError}))
@_(call_with((IndexError(1), ValueError)).returning_transformed(set))
@_(call_with((6,)).raising(TypeError))
@_(call_with(6).raising(TypeError))
def test_un_nest_exceptions(input_value):
    return un_nest_exceptions(input_value)
