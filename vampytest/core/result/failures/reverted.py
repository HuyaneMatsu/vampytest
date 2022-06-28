__all__ = ('get_reverted_failure_message',)

from .helpers import add_documentation_into, add_route_parts_into, render_parameters_into


def get_reverted_failure_message(handle):
    """
    Creates a reverted failure message for the given test handle.
    
    Parameters
    ----------
    handle : ``Handle``
        The test's handle running the test.
    
    Returns
    -------
    failure_message : `str`
    """
    failure_message_parts = []  
    
    failure_message_parts.append('Reverted test passed at: ')
    add_route_parts_into(handle, failure_message_parts)
    
    add_documentation_into(handle, failure_message_parts)
    
    failure_message_parts.append('\nParameters: ')
    render_parameters_into(handle.final_call_state, failure_message_parts)
    
    return ''.join(failure_message_parts)
