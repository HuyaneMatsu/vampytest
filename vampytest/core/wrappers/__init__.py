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

from .aliases import *
from .wrapper_base import *
from .wrapper_call import *
from .wrapper_chainer import *
from .wrapper_conflict import *
from .wrapper_environment import *
from .wrapper_garbage_collect import *
from .wrapper_reverse import *
from .wrapper_skip import *
from .wrapper_skip_conditional import *


__all__ = (
    *aliases.__all__,
    *wrapper_base.__all__,
    *wrapper_call.__all__,
    *wrapper_chainer.__all__,
    *wrapper_conflict.__all__,
    *wrapper_environment.__all__,
    *wrapper_garbage_collect.__all__,
    *wrapper_reverse.__all__,
    *wrapper_skip.__all__,
    *wrapper_skip_conditional.__all__,
)
