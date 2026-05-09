"""
Test wrappers used to enhance our test experience.

Examples
--------
```
import vampytest

def test_equals():
    vampytest.assert_eq(5, 5)


def test_raises():
    with vampytest.assert_raises(TypeError):
        'nice' + 69

def test_contains():
    vampytest.assert_in(range(7), 5)
```
"""
from .assertion_base import *
from .assertion_conditional_base import *
from .assertion_contains import *
from .assertion_equals import *
from .assertion_false import *
from .assertion_identical import *
from .assertion_instance import *
from .assertion_not_contains import *
from .assertion_not_equals import *
from .assertion_not_identical import *
from .assertion_raising import *
from .assertion_states import *
from .assertion_subtype import *
from .assertion_true import *
from .exception import *
from .top_level import *


__all__ = (
    *assertion_raising.__all__,
    *assertion_base.__all__,
    *assertion_conditional_base.__all__,
    *assertion_contains.__all__,
    *assertion_equals.__all__,
    *assertion_false.__all__,
    *assertion_identical.__all__,
    *assertion_instance.__all__,
    *assertion_not_contains.__all__,
    *assertion_not_equals.__all__,
    *assertion_not_identical.__all__,
    *assertion_states.__all__,
    *assertion_subtype.__all__,
    *assertion_true.__all__,
    *exception.__all__,
    *top_level.__all__,
)
