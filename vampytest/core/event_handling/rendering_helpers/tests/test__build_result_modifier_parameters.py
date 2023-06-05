from vampytest import _, call_with

from ..result_modifier_parameters import build_result_modifier_parameters


@_(call_with(None).returning(''))
@_(call_with((None, None),).returning(''))
@_(call_with((None, {'a': 'b'}),).returning('[a = \'b\']'))
@_(call_with((['a'], None),).returning('[\'a\']'))
@_(call_with((['a', 'b'], {'a': 'b', 'c': 'd'}),).returning('[\'a\', \'b\', a = \'b\', c = \'d\']'))
def test__build_result_modifier_parameters(parameters):
    return build_result_modifier_parameters(parameters)
