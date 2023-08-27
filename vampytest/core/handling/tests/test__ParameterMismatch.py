from scarletio import CallableAnalyzer

from ...assertions import assert_eq, assert_in, assert_instance, assert_ne, assert_not_in

from ..parameter_mismatch import ParameterMismatch


def _assert_fields_set(parameter_mismatch):
    """
    Checks whether ``ParameterMismatch`` has every of its parameters set.
    
    Parameters
    ----------
    parameter_mismatch : ``ParameterMismatch``
        The parameter mismatch to test.
    """
    assert_instance(parameter_mismatch, ParameterMismatch)
    assert_instance(parameter_mismatch.extra_keyword_parameters, dict, nullable = True)
    assert_instance(parameter_mismatch.extra_positional_parameters, list, nullable = True)
    assert_instance(parameter_mismatch.keyword_parameters, dict, nullable = True)
    assert_instance(parameter_mismatch.parameters, list)
    assert_instance(parameter_mismatch.positional_parameters, list, nullable = True)
    assert_instance(parameter_mismatch.unsatisfied_parameters, list, nullable = True)


def test__ParameterMismatch__new():
    """
    Tests whether ``ParameterMismatch.__new__`` works as intended.
    """
    def a(p0, p1, p3): pass
    
    parameter_0, parameter_1, parameter_2 = CallableAnalyzer(a).parameters
    
    parameters = [parameter_0, parameter_1, parameter_2]
    positional_parameters = ['koishi', 'orin']
    keyword_parameters = {'satori': 'smug', 'okuu': 'unyu'}
    unsatisfied_parameters = [parameter_2]
    extra_positional_parameters = ['orin']
    extra_keyword_parameters = {'satori': 'smug'}
    
    parameter_mismatch = ParameterMismatch(
        parameters, 
        positional_parameters,
        keyword_parameters,
        unsatisfied_parameters,
        extra_positional_parameters,
        extra_keyword_parameters,
    )
    _assert_fields_set(parameter_mismatch)
    
    assert_eq(parameter_mismatch.extra_keyword_parameters, extra_keyword_parameters)
    assert_eq(parameter_mismatch.extra_positional_parameters, extra_positional_parameters)
    assert_eq(parameter_mismatch.keyword_parameters, keyword_parameters)
    assert_eq(parameter_mismatch.parameters, parameters)
    assert_eq(parameter_mismatch.positional_parameters, positional_parameters)
    assert_eq(parameter_mismatch.unsatisfied_parameters, unsatisfied_parameters)


def test__ParameterMismatch__repr__clean():
    """
    Tests whether ``ParameterMismatch.__repr__`` works as intended.
    
    Case: Clean.
    """
    parameter_mismatch = ParameterMismatch([], None, None, None, None, None)
    
    output = repr(parameter_mismatch)
    assert_instance(output, str)
    
    assert_in(parameter_mismatch.__class__.__name__, output)
    assert_in('parameters = ', output)
    assert_not_in('positional_parameters = ', output)
    assert_not_in('keyword_parameters = ', output)
    assert_not_in('unsatisfied_parameters = ', output)
    assert_not_in('extra_positional_parameters = ', output)
    assert_not_in('extra_keyword_parameters = ', output)



def test__ParameterMismatch__repr__full():
    """
    Tests whether ``ParameterMismatch.__repr__`` works as intended.
    
    Case: Fulled.
    """
    def a(p0, p1, p3): pass
    
    parameter_0, parameter_1, parameter_2 = CallableAnalyzer(a).parameters
    
    parameters = [parameter_0, parameter_1, parameter_2]
    positional_parameters = ['koishi', 'orin']
    keyword_parameters = {'satori': 'smug', 'okuu': 'unyu'}
    unsatisfied_parameters = [parameter_2]
    extra_positional_parameters = ['orin']
    extra_keyword_parameters = {'satori': 'smug'}
    
    parameter_mismatch = ParameterMismatch(
        parameters, 
        positional_parameters,
        keyword_parameters,
        unsatisfied_parameters,
        extra_positional_parameters,
        extra_keyword_parameters,
    )
    
    output = repr(parameter_mismatch)
    assert_instance(output, str)
    
    assert_in(parameter_mismatch.__class__.__name__, output)
    assert_in('parameters = ', output)
    assert_in('positional_parameters = ', output)
    assert_in('keyword_parameters = ', output)
    assert_in('unsatisfied_parameters = ', output)
    assert_in('extra_positional_parameters = ', output)
    assert_in('extra_keyword_parameters = ', output)


def test__ParameterMismatch__eq():
    """
    Tests whether ``ParameterMismatch.__eq__`` works as intended.
    """
    def a(p0, p1, p3): pass
    
    parameter_0, parameter_1, parameter_2 = CallableAnalyzer(a).parameters
    
    keyword_parameters = {
        'parameters': [parameter_0, parameter_1, parameter_2],
        'positional_parameters': ['koishi', 'orin'],
        'keyword_parameters': {'satori': 'smug', 'okuu': 'unyu'},
        'unsatisfied_parameters': [parameter_2],
        'extra_positional_parameters': ['orin'],
        'extra_keyword_parameters': {'satori': 'smug'},
    }
    
    parameter_mismatch = ParameterMismatch(**keyword_parameters)
    
    assert_eq(parameter_mismatch, parameter_mismatch)
    assert_ne(parameter_mismatch, object())
    
    for field_name, field_value in (
        ('parameters', [parameter_0, parameter_1]),
        ('positional_parameters', ['koishi', 'okuu']),
        ('keyword_parameters', {'satori': 'smug', 'okuu': 'smug'}),
        ('unsatisfied_parameters', [parameter_1]),
        ('extra_positional_parameters', ['okuu']),
        ('extra_keyword_parameters', {'satori': 'unyu'}),
    ):
        test_parameter_mismatch = ParameterMismatch(**{**keyword_parameters, field_name: field_value})
        assert_ne(parameter_mismatch, test_parameter_mismatch)
