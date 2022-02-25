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

from .exceptions import *
from .wrapper_base import *
from .wrapper_parameterised import *
from .wrapper_parameterised_returning import *
from .wrapper_returning import *
from .wrapper_skip import *
from .wrapper_skip_conditional import *
from .wrapper_test_marker import *

from .wrapper_parameterised import WrapperParameterised as with_parameters
from .wrapper_returning import WrapperReturning as returning
from .wrapper_skip import WrapperSkip as skip
from .wrapper_skip_conditional import WrapperSkipConditional as skip_if
from .wrapper_test_marker import WrapperTestMarker as mark_as_test

__all__ = (
    'mark_as_test'
    'returning',
    'skip',
    'skip_if',
    'with_parameters',
    
    *exceptions.__all__,
    *wrapper_base.__all__,
    *wrapper_parameterised.__all__,
    *wrapper_parameterised_returning.__all__,
    *wrapper_returning.__all__,
    *wrapper_skip.__all__,
    *wrapper_skip_conditional.__all__,
    *wrapper_test_marker.__all__,
)
