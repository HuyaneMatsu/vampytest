__all__ = (
    'apply_environments_for_file_at', 'set_global_environment', 'set_directory_environment', 'set_file_environment'
)

from os.path import basename as get_file_name, dirname as get_directory_name

from scarletio import get_last_module_frame

from .default import DefaultEnvironment


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
    scope : `int`
        The scope of the storage.
    detail : `str`
        Additional detail for lookup.
        
    Raises
    ------
    TypeError
        - If `environment`'s type is incorrect.
    """
    _check_environment_type(environment)
    
    try:
        environment_by_detail = ENVIRONMENTS_BY_SCOPE[scope]
    except KeyError:
        environment_by_detail = {}
        ENVIRONMENTS_BY_SCOPE[scope] = environment_by_detail
    
    try:
        environments_by_identifier = environment_by_detail[detail]
    except KeyError:
        environments_by_identifier = {}
        environment_by_detail[detail] = environments_by_identifier
    
    environments_by_identifier[environment.identifier] = environment


def _get_last_module_file_path():
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


def set_global_environment(environment):
    """
    Sets an environment for global scope.
    
    Parameters
    ----------
    environment : ``Environment``
        The environment to set.
        
    Raises
    ------
    TypeError
        - If `environment`'s type is incorrect.
    """
    return _set_environment_by_scope(environment, ENVIRONMENT_SCOPE_GLOBAL, '')


def set_directory_environment(environment):
    """
    Sets an environment for directory scope.
    
    Parameters
    ----------
    environment : ``Environment``
        The environment to set.
    
    Raises
    ------
    RuntimeError
        - If not called from an `__init__.py` file.
    TypeError
        - If `environment`'s type is incorrect.
    """
    file_path = _get_last_module_file_path()
    if file_path is None:
        raise RuntimeError(
            f'Cannot set directory level environment, top level file could not be detected successfully.'
        )
    
    if get_file_name(file_path) != '__init__.py':
        raise RuntimeError(
            f'Cannot set directory level environment, top level file is not an `__init__.py` file.'
        )
    
    directory_name = get_directory_name(file_path)
    
    return _set_environment_by_scope(environment, ENVIRONMENT_SCOPE_DIRECTORY, directory_name)


def set_file_environment(environment):
    """
    Sets an environment for directory scope.
    
    Parameters
    ----------
    environment : ``Environment``
        The environment to set.
    
    Raises
    ------
    TypeError
        - If `environment`'s type is incorrect.
    """
    file_path = _get_last_module_file_path()
    if (file_path is None):
        raise RuntimeError(
            f'Cannot set file level environment, top level file could not be detected successfully.'
        )
    
    return _set_environment_by_scope(environment, ENVIRONMENT_SCOPE_FILE, file_path)


def _iter_environments_for_file_at(path):
    """
    Iterates  over the registered environments for the given `path`.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    path : `str`
        The respective file's path.
    """
    # Global
    try:
        environment_by_detail = ENVIRONMENTS_BY_SCOPE[ENVIRONMENT_SCOPE_GLOBAL]
    except KeyError:
        pass
    else:
        try:
            environments_by_identifier = environment_by_detail['']
        except KeyError:
            pass
        else:
            yield from environments_by_identifier.values()
    
    # Directory
    try:
        environment_by_detail = ENVIRONMENTS_BY_SCOPE[ENVIRONMENT_SCOPE_DIRECTORY]
    except KeyError:
        pass
    else:
        directory_name = get_directory_name(path)
        
        try:
            environments_by_identifier = environment_by_detail[directory_name]
        except KeyError:
            pass
        else:
            yield from environments_by_identifier.values()
    
    # File
    try:
        environment_by_detail = ENVIRONMENTS_BY_SCOPE[ENVIRONMENT_SCOPE_FILE]
    except KeyError:
        pass
    else:
        try:
            environments_by_identifier = environment_by_detail[path]
        except KeyError:
            pass
        else:
            yield from environments_by_identifier.values()


def apply_environments_for_file_at(environment_manager, path):
    """
    Applies environments on the given manager for the given path.
    
    Parameters
    ----------
    environment_manager : ``EnvironmentManager``
        The environmental manager to alter.
    path : `str`
        The respective file's path.
    
    Returns
    -------
    environment_manager : ``EnvironmentManager``
    """
    return environment_manager.with_environment(*_iter_environments_for_file_at(path))


def _check_environment_type(environment):
    """
    Checks whether the given `environment` is really an environment.
    
    Parameters
    ----------
    environment : ``Environment``
    
    Raises
    ------
    TypeError
        - If `environment`'s type is incorrect.
    """
    if not isinstance(environment, DefaultEnvironment):
        # Check whether they forgot to instance it.
        # If we just drop a random type error, they wont find what they messed up.
        if isinstance(environment, type) and issubclass(environment, DefaultEnvironment):
            raise TypeError(
                f'You wanted to register an environment without instancing it, '
                f'got {environment.__name__}'
            )
        
        raise TypeError(
            f'`environment` can be `{DefaultEnvironment.__name__}`, '
            f'got {environment.__class__.__name__}; {environment!r}.'
        )
