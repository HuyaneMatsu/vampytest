from vampytest import assert_instance, call_with

from ..result_modifier_parameters import render_result_modifier_parameters


@call_with(None)
@call_with((None, None),)
@call_with((None, {'a': 'b'}),)
@call_with((['a'], None),)
@call_with((['a', 'b'], {'a': 'b', 'c': 'd'}),)
def test__render_result_modifier_parameters(parameters):
    output = render_result_modifier_parameters([], parameters)
    assert_instance(output, list)
    
    for value in output:
        assert_instance(value, str)
