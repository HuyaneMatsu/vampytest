__all__ = ('call_with', 'in_environment', 'raising', 'returning', 'reverse', 'revert', 'skip', 'skip_if', 'with_gc',)

import warnings

from .wrapper_call import WrapperCall
from .wrapper_environment import WrapperEnvironment
from .wrapper_garbage_collect import WrapperGarbageCollect
from .wrapper_reverse import WrapperReverse
from .wrapper_skip import WrapperSkip
from .wrapper_skip_conditional import WrapperSkipConditional


call_with = WrapperCall.call_with_constructor
in_environment = WrapperEnvironment
raising = WrapperCall.raising_constructor
returning = WrapperCall.returning_constructor
reverse = WrapperReverse
skip = WrapperSkip
skip_if = WrapperSkipConditional
with_gc = WrapperGarbageCollect


def revert(*pp, **kp):
    """
    Deprecated and will be removed in 2024 February. Please use ``.reverse`` instead.
    """
    warnings.warn(
        (
            f'`revert` is deprecated and will be removed in 2024 February. '
            f'Please use `.reverse` instead.'
        ),
        FutureWarning,
        stacklevel = 2,
    )
    return reverse(*pp, **kp)
