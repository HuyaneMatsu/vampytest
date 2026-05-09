from vampytest import _, call_with

from ..un_nesting import iter_un_nest


@_(call_with(1).returning([1]))
@_(call_with(()).returning([]))
@_(call_with((1, 2)).returning([2, 1]))
@_(call_with((1, (2, 3))).returning([3, 2, 1]))
@_(call_with((1, 1)).returning([1, 1]))
def test__iter_un_nest(input_value):
    return [*iter_un_nest(input_value)]
