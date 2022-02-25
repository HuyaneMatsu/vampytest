"""
Test assertions

Examples
--------
```
import vampytest


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
from .wrapper_call import *
from .wrapper_skip import *
from .wrapper_skip_conditional import *

returning = WrapperCall.returning_constructor
raising = WrapperCall.raising_constructor
call_with = WrapperCall.call_with_constructor

from .wrapper_skip import WrapperSkip as skip
from .wrapper_skip_conditional import WrapperSkipConditional as skip_if

__all__ = (
    'raising',
    'returning',
    'skip',
    'skip_if',
    'call_with',
    
    *exceptions.__all__,
    *helpers.__all__,
    *wrapper_base.__all__,
    *wrapper_call.__all__,
    *wrapper_skip.__all__,
    *wrapper_skip_conditional.__all__,
)
