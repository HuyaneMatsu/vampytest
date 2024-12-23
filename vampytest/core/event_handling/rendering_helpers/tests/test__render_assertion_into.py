from scarletio import DEFAULT_ANSI_HIGHLIGHTER

from ....assertions import (
    AssertionBase, AssertionContains, AssertionEquals, AssertionIdentical, AssertionInstance, AssertionNotContains,
    AssertionNotEquals, AssertionNotIdentical, AssertionRaising, AssertionSubtype, AssertionValueEvaluationFalse,
    AssertionValueEvaluationTrue, assert_eq, assert_instance
)
from ....utils import _
from ....wrappers import call_from

from ..assertion_rendering import render_assertion_into


def _iter_options():
    # AssertionContains -> default
    assertion = AssertionContains(0, [1])
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 in value_1\n'
            'value_0 = 0\n'
            'value_1 = [1]\n'
        ),
    )
    
    # AssertionContains -> reverse
    assertion = AssertionContains(12, [12], reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 in value_1\n'
            'value_0 = 12\n'
            'value_1 = [12]\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionContains -> highlighted
    assertion = AssertionContains(0, [1])
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = value_0 in value_1\n'
            'value_0 = 0\n'
            'value_1 = [1]\n'
        ),
    )
    
    # AssertionEquals -> default
    assertion = AssertionEquals(0, 1)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 == value_1\n'
            'value_0 = 0\n'
            'value_1 = 1\n'
        ),
    )
    
    # AssertionEquals -> reverse
    assertion = AssertionEquals(12, 12, reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 == value_1\n'
            'value_0 = 12\n'
            'value_1 = 12\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionEquals -> highlighted
    assertion = AssertionEquals(0, 1)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = value_0 == value_1\n'
            'value_0 = 0\n'
            'value_1 = 1\n'
        ),
    )
    
    # AssertionValueEvaluationFalse -> default
    assertion = AssertionValueEvaluationFalse(12)
    
    yield (
        assertion,
        None,
        (
            'operation = not bool(value)\n'
            'value = 12\n'
        ),
    )
    
    # AssertionValueEvaluationFalse -> reverse
    assertion = AssertionValueEvaluationFalse(0, reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = not bool(value)\n'
            'value = 0\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionValueEvaluationFalse -> highlighted
    assertion = AssertionValueEvaluationFalse(12)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = not bool(value)\n'
            'value = 12\n'
        ),
    )
    
    # AssertionValueEvaluationTrue -> default
    assertion = AssertionValueEvaluationTrue(0)
    
    yield (
        assertion,
        None,
        (
            'operation = bool(value)\n'
            'value = 0\n'
        ),
    )
    
    # AssertionValueEvaluationTrue -> reverse
    assertion = AssertionValueEvaluationTrue(12, reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = bool(value)\n'
            'value = 12\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionValueEvaluationTrue -> highlighted
    assertion = AssertionValueEvaluationTrue(0)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = bool(value)\n'
            'value = 0\n'
        ),
    )
    
    # AssertionIdentical -> default
    assertion = AssertionIdentical(1, 2)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 is value_1\n'
            'value_0 = 1\n'
            'value_1 = 2\n'
        ),
    )
    
    # AssertionIdentical -> reverse
    assertion = AssertionIdentical(None, None, reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 is value_1\n'
            'value_0 = None\n'
            'value_1 = None\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionIdentical -> highlighted
    assertion = AssertionIdentical(1, 2)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = value_0 is value_1\n'
            'value_0 = 1\n'
            'value_1 = 2\n'
        ),
    )
    
    # AssertionNotContains -> default
    assertion = AssertionNotContains(0, [12])
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 not in value_1\n'
            'value_0 = 0\n'
            'value_1 = [12]\n'
        ),
    )
    
    # AssertionNotContains -> reverse
    assertion = AssertionNotContains(12, [1], reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 not in value_1\n'
            'value_0 = 12\n'
            'value_1 = [1]\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionNotContains -> highlighted
    assertion = AssertionNotContains(0, [12])
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = value_0 not in value_1\n'
            'value_0 = 0\n'
            'value_1 = [12]\n'
        ),
    )
    
    # AssertionNotEquals -> default
    assertion = AssertionNotEquals(12, 12)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 != value_1\n'
            'value_0 = 12\n'
            'value_1 = 12\n'
        ),
    )
    
    # AssertionNotEquals -> reverse
    assertion = AssertionNotEquals(0, 1, reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 != value_1\n'
            'value_0 = 0\n'
            'value_1 = 1\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionNotEquals -> highlighted
    assertion = AssertionNotEquals(12, 12)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = value_0 != value_1\n'
            'value_0 = 12\n'
            'value_1 = 12\n'
        ),
    )
    
    # AssertionNotIdentical -> default
    assertion = AssertionNotIdentical(None, None)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 is not value_1\n'
            'value_0 = None\n'
            'value_1 = None\n'
        ),
    )
    
    # AssertionNotIdentical -> reverse
    assertion = AssertionNotIdentical(1, 2, reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = value_0 is not value_1\n'
            'value_0 = 1\n'
            'value_1 = 2\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionNotIdentical -> highlighted
    assertion = AssertionNotIdentical(None, None)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = value_0 is not value_1\n'
            'value_0 = None\n'
            'value_1 = None\n'
        ),
    )
    
    # AssertionRaising -> default
    assertion = AssertionRaising(ValueError)
    
    yield (
        assertion,
        None,
        (
            'operation = try except\n'
            'expected_exceptions = ValueError\n'
        ),
    )
    
    # AssertionRaising -> multiple accepted types & instance
    assertion = AssertionRaising(ValueError, IndexError, KeyError(12))
    
    yield (
        assertion,
        None,
        (
            'operation = try except\n'
            'expected_exceptions = IndexError, KeyError(12), ValueError\n'
        ),
    )
    
    
    # AssertionRaising -> accept_subtypes
    assertion = AssertionRaising(ValueError, accept_subtypes = False)
    
    yield (
        assertion,
        None,
        (
            'operation = try except\n'
            'expected_exceptions = ValueError\n'
            'accept_subtypes = False\n'
        ),
    )
    
    
    # AssertionRaising -> where
    where = lambda exception: not exception.args
    assertion = AssertionRaising(ValueError, where = where)
    
    yield (
        assertion,
        None,
        (
            f'operation = try except\n'
            f'expected_exceptions = ValueError\n'
            f'where = {where!r}\n'
        ),
    )
    
    # AssertionRaising -> highlighted
    assertion = AssertionRaising(ValueError)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = try except\n'
            'expected_exceptions = ValueError\n'
        ),
    )
    
    # AssertionInstance -> default
    assertion = AssertionInstance(0, str)
    
    yield (
        assertion,
        None,
        (
            'operation = isinstance(value, expected_types)\n'
            'value = 0\n'
            'expected_types = str\n'
        ),
    )
    
    # AssertionInstance -> multiple expected types.
    assertion = AssertionInstance(0, str, float)
    
    yield (
        assertion,
        None,
        (
            'operation = isinstance(value, expected_types)\n'
            'value = 0\n'
            'expected_types = float, str\n'
        ),
    )
    
    # AssertionInstance -> reverse
    assertion = AssertionInstance(1, int, reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = isinstance(value, expected_types)\n'
            'value = 1\n'
            'expected_types = int\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionInstance -> nullable
    assertion = AssertionInstance(1, str, nullable = True)
    
    yield (
        assertion,
        None,
        (
            'operation = value is None or isinstance(value, expected_types)\n'
            'value = 1\n'
            'expected_types = str\n'
            'nullable = True\n'
        ),
    )
    
    # AssertionInstance -> not accept_subtypes
    assertion = AssertionInstance(True, int, accept_subtypes = False)
    
    yield (
        assertion,
        None,
        (
            'operation = type(value) in expected_types\n'
            'value = True\n'
            'expected_types = int\n'
            'accept_subtypes = False\n'
        ),
    )
    
    # AssertionInstance -> highlighted
    assertion = AssertionInstance(0, str)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = isinstance(value, expected_types)\n'
            'value = 0\n'
            'expected_types = str\n'
        ),
    )
    
    # AssertionSubtype -> default
    assertion = AssertionSubtype(0, str)
    
    yield (
        assertion,
        None,
        (
            'operation = isinstance(value, type) and issubclass(value, expected_types)\n'
            'value = 0\n'
            'expected_types = str\n'
        ),
    )
    
    # AssertionSubtype -> multiple types
    assertion = AssertionSubtype(0, str, float)
    
    yield (
        assertion,
        None,
        (
            'operation = isinstance(value, type) and issubclass(value, expected_types)\n'
            'value = 0\n'
            'expected_types = float, str\n'
        ),
    )
    
    # AssertionSubtype -> reverse
    assertion = AssertionSubtype(1, int, reverse = True)
    
    yield (
        assertion,
        None,
        (
            'operation = isinstance(value, type) and issubclass(value, expected_types)\n'
            'value = 1\n'
            'expected_types = int\n'
            'reverse = True\n'
        ),
    )
    
    # AssertionSubtype -> nullable
    assertion = AssertionSubtype(1, str, nullable = True)
    
    yield (
        assertion,
        None,
        (
            'operation = value is None or isinstance(value, type) and issubclass(value, expected_types)\n'
            'value = 1\n'
            'expected_types = str\n'
            'nullable = True\n'
        ),
    )
    
    # AssertionSubtype -> highlighted
    assertion = AssertionSubtype(0, str)
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            'operation = isinstance(value, type) and issubclass(value, expected_types)\n'
            'value = 0\n'
            'expected_types = str\n'
        ),
    )
    
    # AssertionBase (unknown) -> default
    assertion = AssertionBase()
    
    yield (
        assertion,
        None,
        (
            f'operation = unknown\n'
            f'type = {AssertionBase.__name__}\n'
        ),
    )
    
    # AssertionBase (unknown) -> highlighted
    assertion = AssertionBase()
    
    yield (
        assertion,
        DEFAULT_ANSI_HIGHLIGHTER,
        (
            f'operation = unknown\n'
            f'type = {AssertionBase.__name__}\n'
        ),
    )


@_(call_from(_iter_options()).returning_last())
def test__render_assertion_into(assertion, highlighter):
    """
    Tests whether ``render_assertion_into`` works as intended.
    
    Parameters
    ----------
    assertion : ``AssertionBase``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    output : `str`
    """
    into = render_assertion_into(assertion, highlighter, [])
    
    assert_instance(into, list)
    for element in into:
        assert_instance(element, str)
    
    assert_eq(
        any('\x1b' in element for element in into),
        (highlighter is not None),
    )
    
    return ''.join([element for element in into if '\x1b' not in element])
