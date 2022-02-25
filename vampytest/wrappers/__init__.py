"""
Test assertions

Examples
--------
```
import vampytest

@vampytest.mark_as_test
def is_do_not_have_test_name():
    pass


@vampytest.call_with('cake', 'cake')
def test_is_equal(p1, p2):
    vampytest.assert_equals(p1, p2)


@vampytest.returning('cake')
def test_returning_cake():
    return 'cake'
```
"""

from .exceptions import *
from .helpers import *
from .wrapper_base import *
from .wrapper_combined import *
from .wrapper_skip import *
from .wrapper_skip_conditional import *
from .wrapper_test_marker import *

returning = wrapper_combined.returning_constructor
raising = wrapper_combined.raising_constructor
call_with = wrapper_combined.call_with_constructor

from .wrapper_skip import WrapperSkip as skip
from .wrapper_skip_conditional import WrapperSkipConditional as skip_if
from .wrapper_test_marker import WrapperTestMarker as mark_as_test

__all__ = (
    'mark_as_test'
    'raising',
    'returning',
    'skip',
    'skip_if',
    'call_with',
    
    *exceptions.__all__,
    *helpers.__all__,
    *wrapper_base.__all__,
    *wrapper_combined.__all__,
    *wrapper_parameterised.__all__,
    *wrapper_returning.__all__,
    *wrapper_skip.__all__,
    *wrapper_skip_conditional.__all__,
    *wrapper_test_marker.__all__,
)
