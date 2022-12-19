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

from .wrapper_base import *
from .wrapper_call import *
from .wrapper_chainer import *
from .wrapper_conflict import *
from .wrapper_environment import *
from .wrapper_garbage_collect import *
from .wrapper_revert import *
from .wrapper_skip import *
from .wrapper_skip_conditional import *


returning = WrapperCall.returning_constructor
raising = WrapperCall.raising_constructor
call_with = WrapperCall.call_with_constructor

from .wrapper_environment import WrapperEnvironment as in_environment
from .wrapper_garbage_collect import WrapperGarbageCollect as with_gc
from .wrapper_revert import WrapperRevert as revert
from .wrapper_skip import WrapperSkip as skip
from .wrapper_skip_conditional import WrapperSkipConditional as skip_if


__all__ = (
    'call_with',
    'in_environment',
    'raising',
    'returning',
    'revert',
    'skip',
    'skip_if',
    'with_gc',
    
    *wrapper_base.__all__,
    *wrapper_call.__all__,
    *wrapper_chainer.__all__,
    *wrapper_conflict.__all__,
    *wrapper_environment.__all__,
    *wrapper_garbage_collect.__all__,
    *wrapper_revert.__all__,
    *wrapper_skip.__all__,
    *wrapper_skip_conditional.__all__,
)
