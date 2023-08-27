import operator
import vampytest

# Section 0

@vampytest.returning(True)
def test__values_equal__section_0():
    return 2 == 2


@vampytest.raising(ValueError)
def test_convert_to_int__section_0():
    return int('apple')

# Section 1

@vampytest.returning(True)
@vampytest.call_with(2, 2)
@vampytest.call_with(3, 3)
def test__values_equal__section_1(value_0, value_1):
    return value_0 == value_1


@vampytest.raising(ValueError)
@vampytest.call_with('apple')
@vampytest.call_with('peach')
def test_convert_to_int__section_1(fruit):
    return int(fruit)

# Section 2

@vampytest._(vampytest.call_with('apple').raising(ValueError))
@vampytest._(vampytest.call_with('peach').raising(ValueError))
@vampytest._(vampytest.call_with('12').returning(12))
def test_convert_to_int__section_2(fruit):
    return int(fruit)

# Section 3

@vampytest._(vampytest.call_with(2, 1).returning_transformed(operator.add))
@vampytest._(vampytest.call_with(3, 1).returning_transformed(operator.add))
@vampytest._(vampytest.call_with(4, 3).returning(0))
def test_sum_if_lt_5__section_3(value_0, value_1):
    output = value_0 + value_1
    if output >= 5:
        output = 0
    
    return output

# Section 4

@vampytest._(vampytest.call_from(['apple', 'peach']).raising(ValueError))
@vampytest._(vampytest.call_from(['12', '12']).returning(12))
@vampytest._(vampytest.call_from(['6', '42']).returning_transformed(int))
def test_convert_to_int__section_4(fruit):
    return int(fruit)


def input_and_return_generator():
    yield {'a': 'b'}, 'a', 'b'
    yield {'b': 'c'}, 'b', 'c'


def input_and_exception_generator():
    yield None, None, TypeError
    yield {}, 'a', KeyError
    yield {}, {}, TypeError


@vampytest._(vampytest.call_from(input_and_return_generator()).returning_last())
@vampytest._(vampytest.call_from(input_and_exception_generator()).raising_last())
def test_get_item_fails__section_4(container, key):
    return container[key]
