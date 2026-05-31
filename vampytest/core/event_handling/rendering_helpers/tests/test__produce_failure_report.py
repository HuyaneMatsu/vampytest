from scarletio import DEFAULT_ANSI_HIGHLIGHTER, CallableAnalyzer, get_highlight_streamer, iter_split_ansi_format_codes

from ....assertions import assert_eq, assert_instance, AssertionException, AssertionEquals, AssertionRaising
from ....handling import CallState, ParameterMismatch
from ....utils import _
from ....wrappers import call_from
from ....result import (
    ReportFailureAsserting, ReportFailureParameterMismatch, ReportFailureRaising, ReportFailureReturning,
    ReportBase, ReportOutput

)
from ..report_rendering import produce_failure_report
from ..result_rendering_common import create_break


def _iter_options():
    # produce some cool traceback :D
    def _invoke_assertion(assertion):
        try:
            assertion.invoke()
        except AssertionException as exception:
            return exception
        
        raise RuntimeError
    
    yield (
        'ReportFailureAsserting -> default',
        ReportFailureAsserting(_invoke_assertion(AssertionEquals(0, 1))),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        None,
        (
            f'Assertion failed at: good.pear:test__function\n'
            f'\n'
            f'Assertion traceback (most recent call last):\n'
            f'    File "{__file__}", line {_invoke_assertion.__code__.co_firstlineno + 2}, in {_invoke_assertion.__name__}\n'
            f'        18   | def _invoke_assertion(assertion):\n'
            f'        19   |     try:\n'
            f'        20 >>>         assertion.invoke()\n'
            f'        21   |     except AssertionException as exception:\n'
            f'        22   |         return exception\n'
            f'\n'
            f'operation = value_0 == value_1\n'
            f'value_0 = 0\n'
            f'value_1 = 1\n'
        ),
    )
    
    
    yield (
        'ReportFailureAsserting -> with extras.',
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
    
    
    def _get_exception():
        try:
            raise IndexError(5)
        except IndexError as exception:
            return exception
        
        raise RuntimeError
    
    assertion = AssertionEquals(0, 1)
    assertion.exception = _get_exception()
    
    yield (
        'ReportFailureAsserting -> exception in raising',
        ReportFailureAsserting(AssertionException(assertion)),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            f'Assertion failed at: good.pear:test__function\n'
            f'\n'
            f'Assertion traceback (most recent call last):\n'
            f'\n'
            f'operation = value_0 == value_1\n'
            f'value_0 = 0\n'
            f'value_1 = 1\n'
            f'\n'
            f'Unexpected exception occurred withing the assertion:\n'
            f'----\n'
            f'Traceback (most recent call last):\n'
            f'    File "{__file__}", line {_get_exception.__code__.co_firstlineno + 2}, in {_get_exception.__name__}\n'
            f'        85   | def _get_exception():\n'
            f'        86   |     try:\n'
            f'        87 >>>         raise IndexError(5)\n'
            f'        88   |     except IndexError as exception:\n'
            f'        89   |         return exception\n'
            f'IndexError: 5\n'
        ),
    )
    
    
    def _get_exception():
        try:
            raise IndexError(5)
        except IndexError as exception:
            return exception
        
        raise RuntimeError
    
    assertion = AssertionRaising(KeyError)
    assertion.received_exception = _get_exception()
    
    yield (
        'ReportFailureAsserting -> AssertionRaising -> other exception',
        ReportFailureAsserting(AssertionException(assertion)),
        ('good', 'pear'),
        'test__function',
        None,
        None,
        None,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            f'Assertion failed at: good.pear:test__function\n'
            f'\n'
            f'Assertion traceback (most recent call last):\n'
            f'\n'
            f'operation = try except\n'
            f'expected_exceptions = KeyError\n'
            f'\n'
            f'Captured exception failing the assertion:\n'
            f'----\n'
            f'Traceback (most recent call last):\n'
            f'    File "{__file__}", line {_get_exception.__code__.co_firstlineno + 2}, in {_get_exception.__name__}\n'
            f'        128   | def _get_exception():\n'
            f'        129   |     try:\n'
            f'        130 >>>         raise IndexError(5)\n'
            f'        131   |     except IndexError as exception:\n'
            f'        132   |         return exception\n'
            f'IndexError: 5\n'
        ),
    )
    
    
    yield (
        'ReportFailureAsserting -> with highlighter',
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
    
    
    def _test_function(yukari):
        pass
    
    parameters = CallableAnalyzer(_test_function).parameters
    
    yield (
        'ReportFailureParameterMismatch -> default',
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
            'Unsatisfied function parameters:\n'
            '    yukari\n'
        ),
    )
    
    
    # A little bit of everything :3
    def _test_function(yuyuko, youmu = None, *, ran, chen):
        pass
    
    parameters = CallableAnalyzer(_test_function).parameters
    yield (
        'ReportFailureParameterMismatch -> filled',
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
            'Unsatisfied function parameters:\n'
            '    chen\n'
            '\n'
            'Extra parameters:\n'
            '    \'tea\'\n'
            '    marisa = \'stew\'\n'
        ),
    )
    
    
    def _test_function(yukari):
        pass
    
    parameters = CallableAnalyzer(_test_function).parameters
    
    yield (
        'ReportFailureParameterMismatch -> named',
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
        CallState().with_name('koishi'),
        None,
        None,
        (
            'Parameter mismatch at: good.pear:test__function\n'
            '\n'
            'Named: koishi\n'
            '\n'
            'Function parameters:\n'
            '    yukari\n'
            '\n'
            'Given parameters: N/A\n'
            '\n'
            'Unsatisfied function parameters:\n'
            '    yukari\n'
        ),
    )
    
    
    def _test_function(yukari):
        pass
    
    parameters = CallableAnalyzer(_test_function).parameters
    
    yield (
        'ReportFailureParameterMismatch -> highlighted',
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
            'Unsatisfied function parameters:\n'
            '    yukari\n'
        ),
    )
    
    
    # To insert traceback :D
    def _get_received_exception():
        try:
            raise IndexError(5)
        except IndexError as exception:
            return exception
        
        raise RuntimeError
    
    
    yield (
        'ReportFailureRaising -> default',
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
            f'Unexpected exception at: good.pear:test__function\n'
            f'\n'
            f'expected_exceptions = ValueError\n'
            f'accept_subtypes = False\n'
            f'----\n'
            f'Traceback (most recent call last):\n'
            f'    File "{__file__}", line {_get_received_exception.__code__.co_firstlineno + 2}, in {_get_received_exception.__name__}\n'
            f'        350   | def _get_received_exception():\n'
            f'        351   |     try:\n'
            f'        352 >>>         raise IndexError(5)\n'
            f'        353   |     except IndexError as exception:\n'
            f'        354   |         return exception\n'
            f'IndexError: 5\n'
        ),
    )
    
    
    yield (
        'ReportFailureRaising -> no expected',
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
    
    
    yield (
        'ReportFailureRaising -> no received',
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
    
    
    yield (
        'ReportFailureRaising -> with extras',
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
    
    
    yield (
        'ReportFailureRaising -> with highlighter',
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
    
    
    yield (
        'ReportFailureReturning -> default',
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
    
    
    yield (
        'ReportFailureReturning -> with extras',
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
    
    
    yield (
        'ReportFailureReturning -> with highlighter',
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


@_(call_from(_iter_options()).named_first().returning_last())
def test__produce_failure_report(
    report, path_parts, name, documentation_lines, call_state, output_report, highlighter
):
    """
    Tests whether ``produce_failure_report`` works as intended.
    
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
    
    call_state : ``None | CallState``
        Call state of the report.
    
    output_report : ``None | ReportOutput``
        Output report if any.
    
    highlighter : ``None | HighlightFormatterContext``
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    def create_break_mock(character):
        return character * 4
    
    highlight_streamer = get_highlight_streamer(highlighter)
    output = []
    
    create_break_code_original = create_break.__code__
    try:
        create_break.__code__ = create_break_mock.__code__
        
        for item in produce_failure_report(report, path_parts, name, documentation_lines, call_state, output_report):
            output.extend(highlight_streamer.asend(item))
    finally:
        create_break.__code__ = create_break_code_original
    
    output.extend(highlight_streamer.asend(None))
    
    for element in output:
        assert_instance(element, str)
    
    output_string = ''.join(output)
    split = [*iter_split_ansi_format_codes(output_string)]
    assert_eq(
        any(item[0] for item in split),
        (highlighter is not None),
    )
    
    return ''.join([item[1] for item in split if not item[0]])
