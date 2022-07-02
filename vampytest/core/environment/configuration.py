__all__ = ('set_global_environment', 'set_directory_environment', 'set_file_environment')

from os.path import dirname as get_directory_name

from scarletio import get_last_module_frame


ENVIRONMENT_SCOPE_GLOBAL = 1
ENVIRONMENT_SCOPE_DIRECTORY = 2
ENVIRONMENT_SCOPE_FILE = 3


ENVIRONMENTS_BY_SCOPE = {}


def _set_environment_by_scope(environment, scope, detail):
    """
    Stores an environment.
    
    Parameters
    ----------
    environment : ``Environment``
        The environment to store.
    scope : `inŧ`
        The scope of the storage.
    detail : `None`, `str`
        Additional detail for lookup.
    """
    try:
        environment_by_detail = ENVIRONMENTS_BY_SCOPE[scope]
    except KeyError:
        environment_by_detail = {}
        ENVIRONMENTS_BY_SCOPE[scope] = environment_by_detail
    
    try:
        environments_by_type = environment_by_detail[detail]
    except KeyError:
        environments_by_type = {}
        environment_by_detail[detail] = environments_by_type
    
    environments_by_type[environment.type] = environment


def _get_last_module_file_name():
    """
    Gets the file name of the module from where the last function was called.
    
    Returns
    -------
    file_name : `None`, `str`
    """
    frame = get_last_module_frame()
    if (frame is None):
        return None
    
    spec = frame.f_globals.get('__spec__', None)
    if spec is None:
        return None
    
    return spec.origin


def _get_last_module_directory_name():
    """
    Gets the directory's name of the module from where the last function was called.
    
    Returns
    -------
    file_name : `None`, `str`
    """
    file_name = _get_last_module_file_name()
    if file_name is not None:
        return get_directory_name(file_name)



def set_global_environment(environment):
    """
    Sets an environment for global scope.
    
    Parameters
    ----------
    environment : ``Environment``
        The environment to set.
    """
    return _set_environment_by_scope(environment, ENVIRONMENT_SCOPE_GLOBAL, None)


def set_directory_environment(environment, *, directory_name=None):
    """
    Sets an environment for directory scope.
    
    Parameters
    ----------
    environment : ``Environment``
        The environment to set.
    
    directory_name : `None`, `str` = `None`, Optional (Keyword only)
        The directory's name to where the environment should be set,
        
        If not given will use the last module's directory from where you called it.
    """
    if (directory_name is None):
        directory_name = _get_last_module_directory_name()
        if (directory_name is None):
            raise RuntimeError(
                f'Cannot set directory level environment, top level file could not be detected successfully.'
            )
    
    return _set_environment_by_scope(environment, ENVIRONMENT_SCOPE_DIRECTORY, directory_name)


def set_file_environment(environment, *, file_name=None):
    """
    Sets an environment for directory scope.
    
    Parameters
    ----------
    environment : ``Environment``
        The environment to set.
    
    file_name : `None`, `str` = `None`, Optional (Keyword only)
        The file's name to where the environment should be set,
        
        If not given will use the last module's file from where you called it.
    """
    if (file_name is None):
        file_name = _get_last_module_file_name()
        if (file_name is None):
            raise RuntimeError(
                f'Cannot set file level environment, top level file could not be detected successfully.'
            )
    
    return _set_environment_by_scope(environment, ENVIRONMENT_SCOPE_FILE, file_name)
