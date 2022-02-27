__all__ = ('execute_from_terminal',)

from os import getcwd as get_current_working_directory, sep as PATH_SEPARATOR
from os.path import exists, isabs as is_absolute_path, join as join_paths

from ..core import run_tests_in


def split_path(path):
    """
    Slits the given path removing empty parts.
    
    Parameters
    ----------
    path : `str`
        The path to split.
    
    Returns
    -------
    path_parts : `list` of `str`
    """
    return [path_part for path_part in path.split(PATH_SEPARATOR) if path_part]


def get_base_and_target_path(parameters, index):
    """
    Tries to get the base path of the test and the tests' source path.
    
    Parameters
    ----------
    parameters : `list` of `str`
        Command line parameters.
    index : `int`
        The parameter's index to use.
    
    Returns
    -------
    base_path : `str`
        The path to base our root from.
    test_collection_route : `list` of `str`
        The path parts from base path to collect tests from.
    index : `int`
        The next parameter's index to use.
    
    Raises
    ------
    RuntimeError
        Path not exists.
    """
    parameter_count = len(parameters)

    path_parameter_1 = None
    path_parameter_2 = None
    
    if parameter_count > index:
        maybe_path = parameters[index]
        if not maybe_path.startswith('-'):
            path_parameter_1 = maybe_path
            index += 1
            
            if parameter_count > index:
                if not maybe_path.startswith('-'):
                    maybe_path = parameters[index]
                    path_parameter_2 = maybe_path
                    index += 1
    
    
    if path_parameter_1 is None:
        base_path = get_current_working_directory()
        test_collection_route = []
    
    else:
        path_parameter_1_is_absolute = is_absolute_path(path_parameter_1)
        if path_parameter_1_is_absolute:
            if not exists(path_parameter_1):
                raise RuntimeError(f'Path not exists: {path_parameter_1!r}.')
        
        if path_parameter_2 is None:
            if path_parameter_1_is_absolute:
                base_path = path_parameter_1
                
                test_collection_route = []
            else:
                base_path = get_current_working_directory()
                
                path_to_check_out = join_paths(base_path, path_parameter_1)
                if not exists(path_to_check_out):
                    raise RuntimeError(f'Path not exists: {path_to_check_out!r}.')
                
                test_collection_route = split_path(path_parameter_1)
        
        else:
            path_parameter_2_is_absolute = is_absolute_path(path_parameter_2)
            if not exists(path_parameter_2):
                raise RuntimeError(f'Path not exists: {path_parameter_2!r}.')
            
            if path_parameter_1_is_absolute:
                if path_parameter_2_is_absolute:
                    if not path_parameter_2.startswith(path_parameter_1):
                        raise RuntimeError(
                            f'Path 1 must be sub-path of path 2, got: {path_parameter_1}; {path_parameter_2}.'
                        )
                    
                    base_path = path_parameter_1
                    test_collection_route = split_path(path_parameter_2[len(path_parameter_1):])
                
                else:
                    path_to_check_out = join_paths(path_parameter_1, path_parameter_2)
                    if not exists(path_to_check_out):
                        raise RuntimeError(f'Path not exists: {path_to_check_out!r}.')
                    
                    base_path = path_parameter_1
                    test_collection_route = split_path(path_parameter_2)
            
            else:
                if path_parameter_2_is_absolute:
                    raise RuntimeError(
                        f'Path 1 must be absolute if 2 is, got: {path_parameter_1}; {path_parameter_2}.'
                    )
                
                else:
                    path_to_check_out = join_paths(get_current_working_directory(), path_parameter_1)
                    if not exists(path_to_check_out):
                        raise RuntimeError(f'Path not exists: {path_to_check_out!r}.')
                    
                    base_path = path_to_check_out
    
                    path_to_check_out = join_paths(base_path, path_parameter_2)
                    if not exists(path_to_check_out):
                        raise RuntimeError(f'Path not exists: {path_to_check_out!r}.')
                    
                    test_collection_route = split_path(path_parameter_2)
                    
    return base_path, test_collection_route, index


def execute_from_terminal(parameters):
    """
    Executes vampytest from terminal.
    
    Parameters
    ----------
    parameters : `list` of `str`
        Command line parameters.
    
    Raises
    ------
    RuntimeError
        Path not exists.
    """
    base_path, target_path, index = get_base_and_target_path(parameters, 0)
    run_tests_in(base_path, target_path)
