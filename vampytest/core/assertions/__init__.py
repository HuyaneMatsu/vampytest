"""
Test wrappers used to enhance our test experience.

Examples
--------
```
import vampytest

def test_equals():
    vampytest.assert_equals(5, 5)


def test_raises():
    with vampytest.raises(TypeError):
        'nice' + 69

def test_contains():
    vampytest.assert_contains(range(7), 5)
```
"""
from .assertion_base import *
from .assertion_conditional_base import *
from .assertion_contains import *
from .assertion_equals import *
from .assertion_false import *
from .assertion_identity import *
from .assertion_raising import *
from .assertion_states import *
from .assertion_true import *
from .exceptions import *


# Define more friendly names
CONDITION_STATES = assertion_states

from .assertion_contains import AssertionContains as assert_contains
from .assertion_equals import AssertionEquals as assert_eq
from .assertion_equals import AssertionEquals as assert_equals
from .assertion_false import AssertionValueEvaluationFalse as assert_false
from .assertion_identity import AssertionIdentity as assert_identity
from .assertion_raising import AssertionRaising as assert_raises
from .assertion_true import AssertionValueEvaluationTrue as assert_true


__all__ = (
    'CONDITION_STATES',
    'assert_contains',
    'assert_eq',
    'assert_equals',
    'assert_false',
    'assert_identity',
    'assert_raises',
    'assert_true',
    
    *assertion_raising.__all__,
    *assertion_base.__all__,
    *assertion_conditional_base.__all__,
    *assertion_contains.__all__,
    *assertion_equals.__all__,
    *assertion_false.__all__,
    *assertion_identity.__all__,
    *assertion_states.__all__,
    *assertion_true.__all__,
    *exceptions.__all__,
)
