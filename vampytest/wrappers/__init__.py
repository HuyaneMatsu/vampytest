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

from .base import *


__all__ = (
    *base.__all__,
)
