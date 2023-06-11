import sys


if 'vampytest' in sys.modules:
    from vampytest import ScarletioCoroutineEnvironment, assert_is, set_global_environment
    
    # import event loop
    # from somewhere import EVENT_LOOP
    from scarletio import create_event_loop
    EVENT_LOOP = create_event_loop()
    
    
    set_global_environment(ScarletioCoroutineEnvironment(event_loop = EVENT_LOOP))


# ---- test file ----- #

from scarletio import get_event_loop

import vampytest
from scarletio import get_event_loop

# import event loop
# from somewhere import EVENT_LOOP


# Test whether we are indeed on the correct event loop
async def test_event_loop_same():
    vampytest.assert_is(EVENT_LOOP, get_event_loop())
