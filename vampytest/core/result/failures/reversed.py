__all__ = ('get_reversed_failure_message',)

from .helpers import render_documentation_into, render_route_parts_into, render_parameters_into


def get_reversed_failure_message(handle):
    """
    Creates a reversed failure message for the given test handle.
    
    Parameters
    ----------
    handle : ``Handle``
        The test's handle running the test.
    
    Returns
    -------
    failure_message : `str`
    """
    failure_message_parts = []  
    
    failure_message_parts.append('Reversed test passed at: ')
    failure_message_parts = render_route_parts_into(failure_message_parts, handle)
    failure_message_parts = render_documentation_into(failure_message_parts, handle)
    
    final_call_state = handle.final_call_state
    if (final_call_state is not None) and final_call_state:
        failure_message_parts.append('\nParameters: ')
        failure_message_parts = render_parameters_into(
            failure_message_parts, final_call_state.positional_parameters, final_call_state.keyword_parameters
        )
    
    return ''.join(failure_message_parts)
