"""
Test assertions

Examples
--------
```
import vampytest

@vampytest.mark_as_test
def is_do_not_have_test_name():
    pass


@vampytest.with_parameters('cake', 'cake')
def test_is_equal(p1, p2):
    vampytest.assert_equals(p1, p2)


@vampytest.returning('cake')
def test_returning_cake():
    return 'cake'
```
"""
from .assertion_base import *
from .assertion_conditional_base import *
from .assertion_contains import *
from .assertion_equals import *
from .assertion_states import *
from .exceptions import *


# Define more friendly names
CONDITION_STATES = assertion_states

from .assertion_equals import AssertionEquals as assert_eq
from .assertion_equals import AssertionEquals as assert_equals
from .assertion_contains import AssertionContains as assert_contains


__all__ = (
    'CONDITION_STATES',
    'assert_eq',
    'assert_equals',
    'assert_contains',
    
    *assertion_base.__all__,
    *assertion_conditional_base.__all__,
    *assertion_contains.__all__,
    *assertion_equals.__all__,
    *assertion_states.__all__,
    *exceptions.__all__,
)
