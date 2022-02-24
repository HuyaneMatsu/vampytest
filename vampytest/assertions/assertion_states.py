__all__ = ('get_assertion_state_name', )

NONE = 0
CREATED = 1
FAILED = 2
PASSED = 3

DEFAULT_ASSERTION_STATE_NAME = 'unknown'

ASSERTION_STATE_TO_NAME = {
    NONE: 'none',
    CREATED: 'created',
    FAILED: 'failed',
    PASSED: 'passed',
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
