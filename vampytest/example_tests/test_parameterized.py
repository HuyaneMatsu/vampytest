import vampytest


@vampytest.call_with(2, 2)
@vampytest.call_with(3, 3)
def test__values_equal(value_0, value_1):
    vampytest.assert_eq(value_0, value_1)


def input_generator():
    a = object()
    yield a, a
    
    b = 'apple'
    yield b, b
    
    c = int
    yield c, c


@vampytest.call_from(input_generator())
def test__values_identical(value_0, value_1):
    vampytest.assert_is(value_0, value_1)
