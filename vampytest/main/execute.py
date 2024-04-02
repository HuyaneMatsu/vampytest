__all__ = ('execute_from_parameters',)

import sys
from os import getcwd as get_current_working_directory

from scarletio import write_exception_sync

from ..core import run_tests_in, shutdown_environments
from ..return_codes import RETURN_CODE_TEST_LOCATION_FAILURE, RETURN_CODE_TEST_RUNNER_INTERRUPTED

from .source_lookup import get_source_and_target


def build_error_message(errors, parameters):
    """
    Builds error message for the case when test source could not be identified.
    
    Parameters
    ----------
    errors : `None | list<(str, str)>`
        Found errors while trying to resolve source. In a `path - message` relation.
    parameters : `list<str>`
        Parameters the test would be called with.
    
    Returns
    -------
    error_message : `str`
    """
    error_message_parts = []
    
    error_message_parts.append('Could not detect testing directory.\n')
    
    error_message_parts.append('Working directory: ')
    error_message_parts.append(get_current_working_directory())
    error_message_parts.append('\n')
    
    error_message_parts.append('Parameters: ')
    if parameters:
        for parameter in parameters:
            error_message_parts.append('\n- "')
            error_message_parts.append(parameter.replace('"', '\\"'))
            error_message_parts.append('"')
    
    else:
        error_message_parts.append('*none*')
    error_message_parts.append('\n')
    
    if errors is not None:
        error_message_parts.append('\nErrors while detecting source(s):\n')
        
        for index, (path, error) in enumerate(errors, 1):
            index_string = str(index)
            error_message_parts.append(index_string)
            error_message_parts.append('. ')
            error_message_parts.append('Path: ')
            error_message_parts.append(path)
            error_message_parts.append(' ' * (2 + len(index_string)))
            error_message_parts.append('\n')
            
            error_message_parts.append('Error: ')
            error_message_parts.append(error)
            error_message_parts.append('\n')
    
    return ''.join(error_message_parts)


def execute_from_parameters(parameters):
    """
    Executes vampytest from terminal.
    
    Parameters
    ----------
    parameters : `list` of `str`
        Command line parameters.
    
    Returns
    -------
    return_code : `int`
    """
    source_directory, sources, test_collection_route, errors, index = get_source_and_target(parameters, 0)
    
    if (source_directory is None) or (sources is None):
        sys.stderr.write(build_error_message(errors, parameters))
        return RETURN_CODE_TEST_LOCATION_FAILURE
    
    try:
        return run_tests_in(source_directory, sources, test_collection_route)
    except KeyboardInterrupt as exception:
        write_exception_sync(exception, before = '\nTest running interrupted...')
        return RETURN_CODE_TEST_RUNNER_INTERRUPTED
    
    finally:
        shutdown_environments()
