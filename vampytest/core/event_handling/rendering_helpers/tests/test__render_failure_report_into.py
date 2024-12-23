from scarletio import DEFAULT_ANSI_HIGHLIGHTER, CallableAnalyzer

from ....assertions import assert_eq, assert_instance, AssertionException, AssertionEquals, AssertionRaising
from ....handling import CallState, ParameterMismatch
from ....utils import _
from ....wrappers import call_from
from ....result import (
    ReportFailureAsserting, ReportFailureParameterMismatch, ReportFailureRaising, ReportFailureReturning,
    ReportBase, ReportOutput

)
from ..report_rendering import render_failure_report_into
from ..result_rendering_common import create_break


def _iter_options():
    # ReportFailureAsserting -> default
    
    # produce some cool traceback :D
    def _invoke_assertion(assertion):
        try:
            assertion.invoke()
        except AssertionException as exception:
            return exception
        
        raise RuntimeError
    
    yield (
        ReportFailureAsserting(_invoke_assertion(AssertionEquals(0, 1))),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        None,
        (
            'Assertion failed at: good.pear:test__function\n'
            '\n'
            'Assertion traceback (most recent call last):\n'
            f'  File "{__file__}", line {_invoke_assertion.__code__.co_firstlineno + 2}, in {_invoke_assertion.__name__}\n'
            '    assertion.invoke()\n'
            '\n'
            'operation = value_0 == value_1\n'
            'value_0 = 0\n'
            'value_1 = 1\n'
        ),
    )
    
    # ReportFailureAsserting -> with extras.
    yield (
        ReportFailureAsserting(AssertionException(AssertionEquals(0, 1))),
        ('good', 'pear'),
        'test__function',
        ['hello', 'nyan'],
        CallState().with_parameters([int], None),
        ReportOutput('orin\nokuu\n'),
        None,
        (
            'Assertion failed at: good.pear:test__function\n'
            '\n'
            '> hello\n'
            '> nyan\n'
            '\n'
            'Parameters:\n'
            '    int\n'
            '\n'
            'Assertion traceback (most recent call last):\n'
            '\n'
            'operation = value_0 == value_1\n'
            'value_0 = 0\n'
            'value_1 = 1\n'
            '\n'
            'Captured output while running the test:\n'
            '----\n'
            'orin\n'
            'okuu\n'
        ),
    )
    
    # ReportFailureAsserting -> exception in raising
    
    def _get_exception():
        try:
            raise IndexError(5)
        except IndexError as exception:
            return exception
        
        raise RuntimeError
    
    assertion = AssertionEquals(0, 1)
    assertion.exception = _get_exception()
    
    yield (
        ReportFailureAsserting(AssertionException(assertion)),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Assertion failed at: good.pear:test__function\n'
            '\n'
            'Assertion traceback (most recent call last):\n'
            '\n'
            'operation = value_0 == value_1\n'
            'value_0 = 0\n'
            'value_1 = 1\n'
            '\n'
            'Unexpected exception occurred withing the assertion:\n'
            '----\n'
            'Traceback (most recent call last):\n'
            f'  File "{__file__}", line {_get_exception.__code__.co_firstlineno + 2}, in {_get_exception.__name__}\n'
            '    raise IndexError(5)\n'
            'IndexError: 5\n'
        ),
    )
    # ReportFailureAsserting -> AssertionRaising -> other exception
    
    def _get_exception():
        try:
            raise IndexError(5)
        except IndexError as exception:
            return exception
        
        raise RuntimeError
    
    assertion = AssertionRaising(KeyError)
    assertion.received_exception = _get_exception()
    
    yield (
        ReportFailureAsserting(AssertionException(assertion)),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Assertion failed at: good.pear:test__function\n'
            '\n'
            'Assertion traceback (most recent call last):\n'
            '\n'
            'operation = try except\n'
            'expected_exceptions = KeyError\n'
            '\n'
            'Captured exception failing the assertion:\n'
            '----\n'
            'Traceback (most recent call last):\n'
            f'  File "{__file__}", line {_get_exception.__code__.co_firstlineno + 2}, in {_get_exception.__name__}\n'
            '    raise IndexError(5)\n'
            'IndexError: 5\n'
        ),
    )
    
    # ReportFailureAsserting -> with highlighter
    yield (
        ReportFailureAsserting(AssertionException(AssertionEquals(0, 1))),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Assertion failed at: good.pear:test__function\n'
            '\n'
            'Assertion traceback (most recent call last):\n'
            '\n'
            'operation = value_0 == value_1\n'
            'value_0 = 0\n'
            'value_1 = 1\n'
        ),
    )
    
    # ReportFailureParameterMismatch -> default
    
    def _test_function(yukari):
        pass
    
    parameters = CallableAnalyzer(_test_function).parameters
    
    yield (
        ReportFailureParameterMismatch(ParameterMismatch(
            parameters,
            None,
            None,
            parameters,
            None,
            None,
        )),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        None,
        (
            'Parameter mismatch at: good.pear:test__function\n'
            '\n'
            'Function parameters:\n'
            '    yukari\n'
            '\n'
            'Given parameters: N/A\n'
            '\n'
            'Unsatisfied function parameters:'
            '    yukari\n'
        ),
    )
    
    # ReportFailureParameterMismatch -> filled
    
    # A little bit of everything :3
    def _test_function(yuyuko, youmu = None, *, ran, chen):
        pass
    
    parameters = CallableAnalyzer(_test_function).parameters
    yield (
        ReportFailureParameterMismatch(ParameterMismatch(
            parameters,
            ['pizza', 'steamed buns', 'tea'],
            {'ran': 'pocky', 'marisa': 'stew'},
            [parameters[-1]],
            ['tea'],
            {'marisa': 'stew'}
        )),
        ('good', 'pear'),
        'test__function',
        ['orin', 'okuu'],
        None,
        None,
        None,
        (
            'Parameter mismatch at: good.pear:test__function\n'
            '\n'
            '> orin\n'
            '> okuu\n'
            '\n'
            'Function parameters:\n'
            '    yuyuko\n'
            '    youmu = None\n'
            '    *\n'
            '    ran\n'
            '    chen\n'
            '\n'
            'Given parameters:\n'
            '    \'pizza\'\n'
            '    \'steamed buns\'\n'
            '    \'tea\'\n'
            '    ran = \'pocky\'\n'
            '    marisa = \'stew\'\n'
            '\n'
            'Unsatisfied function parameters:'
            '    chen\n'
            '\n'
            'Extra parameters:\n'
            '    \'tea\'\n'
            '    marisa = \'stew\'\n'
        ),
    )
    
    # ReportFailureParameterMismatch -> highlighted
    
    def _test_function(yukari):
        pass
    
    parameters = CallableAnalyzer(_test_function).parameters
    
    yield (
        ReportFailureParameterMismatch(ParameterMismatch(
            parameters,
            None,
            None,
            parameters,
            None,
            None,
        )),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Parameter mismatch at: good.pear:test__function\n'
            '\n'
            'Function parameters:\n'
            '    yukari\n'
            '\n'
            'Given parameters: N/A\n'
            '\n'
            'Unsatisfied function parameters:'
            '    yukari\n'
        ),
    )
    
    # ReportFailureRaising -> default
    
    # To insert traceback :D
    def _get_received_exception():
        try:
            raise IndexError(5)
        except IndexError as exception:
            return exception
        
        raise RuntimeError
    
    
    yield (
        ReportFailureRaising(
            {ValueError},
            False,
            _get_received_exception(),
        ),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        None,
        (
            'Unexpected exception at: good.pear:test__function\n'
            '\n'
            'expected_exceptions = ValueError\n'
            'accept_subtypes = False\n'
            '----\n'
            'Traceback (most recent call last):\n'
            f'  File "{__file__}", line {_get_received_exception.__code__.co_firstlineno + 2}, in {_get_received_exception.__name__}\n'
            '    raise IndexError(5)\n'
            'IndexError: 5\n'
        ),
    )
    
    # ReportFailureRaising -> no expected
    
    yield (
        ReportFailureRaising(
            None,
            False,
            IndexError(5),
        ),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Unexpected exception at: good.pear:test__function\n'
            '----\n'
            'Traceback (most recent call last):\n'
            'IndexError: 5\n'
        ),
    )
    
    # ReportFailureRaising -> no received
    
    yield (
        ReportFailureRaising(
            {ValueError},
            False,
            None,
        ),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Missing exception at: good.pear:test__function\n'
            '\n'
            'expected_exceptions = ValueError\n'
            'accept_subtypes = False\n'
        ),
    )
    
    # ReportFailureRaising -> with extras
    
    yield (
        ReportFailureRaising(
            {ValueError},
            False,
            IndexError(5),
        ),
        ('good', 'pear'),
        'test__function',
        ['hello', 'nyan'],
        CallState().with_parameters([int], None),
        ReportOutput('orin\nokuu\n'),
        None,
        (
            'Unexpected exception at: good.pear:test__function\n'
            '\n'
            '> hello\n'
            '> nyan\n'
            '\n'
            'Parameters:\n'
            '    int\n'
            '\n'
            'expected_exceptions = ValueError\n'
            'accept_subtypes = False\n'
            '----\n'
            'Traceback (most recent call last):\n'
            'IndexError: 5\n'
            '\n'
            'Captured output while running the test:\n'
            '----\n'
            'orin\n'
            'okuu\n'
        ),
    )
    
    # ReportFailureRaising -> with highlighter
    
    yield (
        ReportFailureRaising(
            {ValueError},
            False,
            IndexError(5),
        ),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Unexpected exception at: good.pear:test__function\n'
            '\n'
            'expected_exceptions = ValueError\n'
            'accept_subtypes = False\n'
            '----\n'
            'Traceback (most recent call last):\n'
            'IndexError: 5\n'
        ),
    )
    
    # ReportFailureReturning -> default
    
    yield (
        ReportFailureReturning(
            1,
            2,
        ),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        None,
        (
            'Unexpected return at: good.pear:test__function\n'
            '\n'
            'expected_return = 1\n'
            'received_return = 2\n'
        ),
    )
    
    # ReportFailureReturning -> with extras
    
    yield (
        ReportFailureReturning(
            1,
            2,
        ),
        ('good', 'pear'),
        'test__function',
        ['hello', 'nyan'],
        CallState().with_parameters([int], None),
        ReportOutput('orin\nokuu\n'),
        None,
        (
            'Unexpected return at: good.pear:test__function\n'
            '\n'
            '> hello\n'
            '> nyan\n'
            '\n'
            'Parameters:\n'
            '    int\n'
            '\n'
            'expected_return = 1\n'
            'received_return = 2\n'
            '\n'
            'Captured output while running the test:\n'
            '----\n'
            'orin\n'
            'okuu\n'
        ),
    )
    
    # ReportFailureReturning -> with highlighter
    
    yield (
        ReportFailureReturning(
            1,
            2,
        ),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'Unexpected return at: good.pear:test__function\n'
            '\n'
            'expected_return = 1\n'
            'received_return = 2\n'
        ),
    )


@_(call_from(_iter_options()).returning_last())
def test__render_failure_report_into(
    report, path_parts, name, documentation_lines, call_state, output_report, highlighter
):
    """
    Tests whether ``render_failure_report_into`` works as intended.
    
    Parameters
    ----------
    report : ``ReportBase``
        Report to render.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state of the report.
    
    output_report : `None | ReportOutput`
        Output report if any.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    def create_break_mock(character):
        return character * 4
    
    create_break_code_original = create_break.__code__
    try:
        create_break.__code__ = create_break_mock.__code__
        
        into = render_failure_report_into(
            report, path_parts, name, documentation_lines, call_state, output_report, highlighter, []
        )
    
    finally:
        create_break.__code__ = create_break_code_original
    
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
