from scarletio import CallableAnalyzer

from ...utils import _
from ...wrappers import call_from

from ..parameter_checking import (
    check_parameter_mismatch, collect_unsatisfied_parameters, exhaust_keyword_parameter,
    exhaust_next_positional_parameter, iter_parameters_to_pass
)
from ..parameter_mismatch import ParameterMismatch


def _iter_options__iter_parameters_to_pass():
    yield None, None, []
    yield (
        ['koishi', 'orin'],
        {'satori': 'smug', 'okuu': 'unyu'},
        [(True, 'koishi'), (True, 'orin'), (False, ('satori', 'smug')), (False, ('okuu', 'unyu'))],
    )


@_(call_from(_iter_options__iter_parameters_to_pass()).returning_last())
def test__iter_parameters_to_pass(positional_parameters, keyword_parameters):
    """
    Tests whether ``iter_parameters_to_pass`` works as intended.
    
    Parameters
    ----------
    positional_parameters : `None | list<object>`
        Positional parameters to call the test with.
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters to call the test with.
    
    Returns
    -------
    output : `list<(bool, object)>`
    """
    return [*iter_parameters_to_pass(positional_parameters, keyword_parameters)]


def _iter_options__exhaust_next_positional_parameter():
    def a(p0, *p1, p2 = 2, **p3):
        pass
    
    parameter_0, parameter_1, parameter_2, parameter_3 = CallableAnalyzer(a).parameters
    
    yield [], (False, [])
    yield [parameter_0], (True, [])
    yield [parameter_0, parameter_0], (True, [parameter_0])
    yield [parameter_1], (True, [parameter_1])
    yield [parameter_2], (False, [parameter_2])
    yield [parameter_3], (False, [parameter_3])


@_(call_from(_iter_options__exhaust_next_positional_parameter()).returning_last())
def test__exhaust_next_positional_parameter(parameters):
    """
    Tests whether ``exhaust_next_positional_parameter`` works as intended.
    
    Parameters
    ----------
    parameters : `list<Parameter>`
        Parameters to exhaust from.
    
    Returns
    -------
    output : `bool`
    new_parameters : `list<Parameter>`
    """
    new_parameters = parameters.copy()
    output = exhaust_next_positional_parameter(new_parameters)
    return output, new_parameters


def _iter_options__exhaust_keyword_parameter():
    def a(p0, *p1, p2 = 2, **p3):
        pass
    
    parameter_0, parameter_1, parameter_2, parameter_3 = CallableAnalyzer(a).parameters
    
    yield [], 'p0', (False, [])
    yield [parameter_0], 'p0', (True, [])
    yield [parameter_0, parameter_0], 'p0', (True, [parameter_0])
    yield [parameter_0], 'p1', (False, [parameter_0])
    yield [parameter_1], 'p1', (False, [parameter_1])
    yield [parameter_2], 'p2', (True, [])
    yield [parameter_2, parameter_2], 'p2', (True, [parameter_2])
    yield [parameter_2], 'p3', (False, [parameter_2])
    yield [parameter_3], 'p2', (True, [parameter_3])
    yield [parameter_3], 'p3', (True, [parameter_3])
    yield [parameter_2, parameter_3], 'p2', (True, [parameter_3])
    yield [parameter_2, parameter_3], 'p4', (True, [parameter_2, parameter_3])


@_(call_from(_iter_options__exhaust_keyword_parameter()).returning_last())
def test__exhaust_keyword_parameter(parameters, name):
    """
    Tests whether ``exhaust_keyword_parameter`` works as intended.
    
    Parameters
    ----------
    parameters : `list<Parameter>`
        Parameters to exhaust from.
    name : `str`
        The parameter's name.
    
    Returns
    -------
    output : `bool`
    new_parameters : `list<Parameter>`
    """
    new_parameters = parameters.copy()
    output = exhaust_keyword_parameter(new_parameters, name)
    return output, new_parameters


def _iter_options__collect_unsatisfied_parameters():
    def a(p0, p1 = None, *p2, p3, p4 = 2, **p5):
        pass

    parameter_0, parameter_1, parameter_2, parameter_3, parameter_4, parameter_5 = CallableAnalyzer(a).parameters
    
    yield [], None
    yield [parameter_1, parameter_2, parameter_4, parameter_5], None
    yield [parameter_0, parameter_1, parameter_2, parameter_3, parameter_4, parameter_5], [parameter_0, parameter_3]
    yield [parameter_0, parameter_3], [parameter_0, parameter_3]


@_(call_from(_iter_options__collect_unsatisfied_parameters()).returning_last())
def test__collect_unsatisfied_parameters(parameters):
    """
    Tests whether ``collect_unsatisfied_parameters`` works as intended.
    
    Parameters
    ----------
    parameters : `list<Parameter>`
        Parameters to exhaust from.
    
    Returns
    -------
    unsatisfied_parameters : `None | list<Parameter>`
    """
    return collect_unsatisfied_parameters(parameters)


def iter_options__check_parameter_mismatch():
    def test_function():
        pass

    yield (
        test_function,
        None,
        None,
        None,
    )
    
    yield (
        test_function,
        ['koishi'],
        {'satori': 'smug'},
        ParameterMismatch(
            [],
            ['koishi'],
            {'satori': 'smug'},
            None,
            ['koishi'],
            {'satori': 'smug'},
        ),   
    )
    
    def test_function(p0, p1 = None, *p2, p3, p4 = 2, **p5):
        pass
    
    parameter_0, parameter_1, parameter_2, parameter_3, parameter_4, parameter_5 = \
        CallableAnalyzer(test_function).parameters
    
    yield (
        test_function,
        ['koishi'],
        {'p3': 'unyu'},
        None,
    )
    
    yield (
        test_function,
        ['koishi', 'satori', 'okuu', 'orin'],
        {'p3': 'unyu', 'p4': 'nyu', 'p6': 'umu'},
        None,
    )
    
    yield (
        test_function,
        None,
        None,
        ParameterMismatch(
            [parameter_0, parameter_1, parameter_2, parameter_3, parameter_4, parameter_5],
            None,
            None,
            [parameter_0, parameter_3],
            None,
            None,
        ),   
    )
    
    
    def test_function(p0, p1, *, p2, p3):
        pass

    parameter_0, parameter_1, parameter_2, parameter_3 = CallableAnalyzer(test_function).parameters

    yield (
        test_function,
        ['koishi', 'satori'],
        {'p2': 'smug', 'p3': 'unyu'},
        None,
    )
    
    yield (
        test_function,
        ['koishi', 'satori', 'okuu', 'orin'],
        {'p2': 'unyu', 'p3': 'nyu', 'p4': 'umu'},
        ParameterMismatch(
            [parameter_0, parameter_1, parameter_2, parameter_3],
            ['koishi', 'satori', 'okuu', 'orin'],
            {'p2': 'unyu', 'p3': 'nyu', 'p4': 'umu'},
            None,
            ['okuu', 'orin'],
            {'p4': 'umu'},
        ), 
    )
    
    yield (
        test_function,
        None,
        None,
        ParameterMismatch(
            [parameter_0, parameter_1, parameter_2, parameter_3],
            None,
            None,
            [parameter_0, parameter_1, parameter_2, parameter_3],
            None,
            None,
        ),   
    )


@_(call_from(iter_options__check_parameter_mismatch()).returning_last())
def test__check_parameter_mismatch(test, positional_parameters, keyword_parameters):
    """
    Tests whether ``check_parameter_mismatch`` works as intended.
    
    Parameters
    ----------
    test : `FunctionType`
        The test to check.
    positional_parameters : `None | list<object`
        Positional parameters to call the test with.
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters to call the test with.
    
    Returns
    -------
    parameter_mismatch : `None`, ``ParameterMismatch``
    """
    return check_parameter_mismatch(test, positional_parameters, keyword_parameters)
