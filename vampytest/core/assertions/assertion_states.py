__all__ = ('get_assertion_state_name', )


ASSERTION_STATE_NONE = 0
ASSERTION_STATE_CREATED = 1
ASSERTION_STATE_FAILED = 2
ASSERTION_STATE_PASSED = 3

DEFAULT_ASSERTION_STATE_NAME = 'unknown'

ASSERTION_STATE_TO_NAME = {
    ASSERTION_STATE_NONE: 'none',
    ASSERTION_STATE_CREATED: 'created',
    ASSERTION_STATE_FAILED: 'failed',
    ASSERTION_STATE_PASSED: 'passed',
}


def get_assertion_state_name(state):
    """
    Returns the condition state's name.
    
    Parameters
    ----------
    state : `int`
        Condition state value.
    
    Returns
    -------
    state_name : `str`
        The condition state's value.
    """
    return ASSERTION_STATE_TO_NAME.get(state, DEFAULT_ASSERTION_STATE_NAME)
