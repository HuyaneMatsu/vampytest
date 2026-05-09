from vampytest import _, call_with

from ..un_nesting import un_nest


@_(call_with(1).returning({1}))
@_(call_with(()).returning_transformed(set))
@_(call_with((1, 2)).returning_transformed(set))
@_(call_with((1, (2, 3))).returning({1, 2, 3}))
@_(call_with((1, 1)).returning_transformed(set))
def test__un_nest(input_value):
    return un_nest(input_value)
