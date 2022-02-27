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
from .assertion_raising import *
from .assertion_states import *
from .exceptions import *


# Define more friendly names
CONDITION_STATES = assertion_states

from .assertion_contains import AssertionContains as assert_contains
from .assertion_equals import AssertionEquals as assert_eq
from .assertion_equals import AssertionEquals as assert_equals
from .assertion_raising import AssertionRaising as assert_raising


__all__ = (
    'CONDITION_STATES',
    'assert_contains',
    'assert_eq',
    'assert_equals',
    'assert_raising',
    
    *assertion_raising.__all__,
    *assertion_base.__all__,
    *assertion_conditional_base.__all__,
    *assertion_contains.__all__,
    *assertion_equals.__all__,
    *assertion_states.__all__,
    *exceptions.__all__,
)
