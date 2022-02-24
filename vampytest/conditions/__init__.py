"""
Test conditions

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
from .condition_base import *
from .condition_equals import *
from .condition_states import *
from .exceptions import *


CONDITION_STATES = condition_states

__all__ = (
    'CONDITION_STATES',
    
    *condition_base.__all__,
    *condition_equals.__all__,
    *condition_states.__all__,
    *exceptions.__all__,
)
