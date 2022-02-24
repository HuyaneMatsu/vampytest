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
from .assertion_equals import *
from .assertion_states import *
from .exceptions import *


CONDITION_STATES = assertion_states

__all__ = (
    'CONDITION_STATES',
    
    *assertion_base.__all__,
    *assertion_conditional_base.__all__,
    *assertion_equals.__all__,
    *assertion_states.__all__,
    *exceptions.__all__,
)
