__all__ = ()

import sys
from os.path import join as join_paths, isfile as is_file
from types import ModuleType
from importlib.util import module_from_spec
from importlib.machinery import ModuleSpec, SourceFileLoader
from os import getcwd as get_current_working_directory, sep as PATH_SEPARATOR
from os.path import dirname as get_parent_directory_path, split as split_path, splitext as split_extension


PYTHON_EXTENSIONS = frozenset(('.py', '.pyd', '.pyc', '.so'))


def has_init(path):
    """
    Returns whether the directory has `__init__.py` file, or something equivalent to it.
    
    Parameters
    ----------
    path : `str`
        The path to check.
    
    Returns
    -------
    has_init : `bool`
    """
    path = join_paths(path, '__init__')
    for python_extension in PYTHON_EXTENSIONS:
        if is_file(path + python_extension):
            return True
    
    return False


def is_directory_project_source(path):
    """
    Returns whether the given directory is a project source.
    
    Parameters
    ----------
    path : `str`
        The path to check.
    
    Returns
    -------
    is_directory_project_source : `bool`
    """
    if is_file(join_paths(path, 'setup.py')):
        return True
    
    if is_file(join_paths(path, 'pyproject.toml')):
        return True
    
    return False


def build_project_sources(module_name, module_packages):
    """
    Builds the project's sources to import.
    
    Parameters
    ----------
    module_name : `object`
        The module's name. Preferably a string.
    module_packages : `object`
        The module's packages. Preferably a list of strings.
    
    Returns
    -------
    project_sources : `None | set<str>`
    """
    project_sources = None
    
    # check `module_packages` if applicable
    if (module_packages is not None) and (getattr(module_packages, '__iter__', None) is not None):
        for module_package in module_packages:
            if not isinstance(module_package, str):
                continue
            
            dot_index = module_package.find('.')
            if dot_index == -1:
                project_source = module_package
            elif dot_index > 0:
                project_source = module_package[:dot_index]
            else:
                continue
            
            if project_sources is None:
                project_sources = set()
            
            project_sources.add(project_source)
    
    # check `module_name` if applicable
    elif (module_name is not None) and isinstance(module_name, str):
        if project_sources is None:
            project_sources = set()
        
        project_sources.add(module_name)
    
    return project_sources


# I ain't gonna write test for this
def execute_setup_file(path):
    """
    Executes a file at the given path. Specifically used for `setup.py` files.
    
    Parameters
    ----------
    path : `str`
        Path to the file.
    """
    try:
        module_specification = ModuleSpec('setup', SourceFileLoader('setup', path), origin = path)
        module_specification.has_location = True
        module = module_from_spec(module_specification)
        module_specification.loader.exec_module(module)
    finally:
        try:
            del sys.modules['setup']
        except KeyError:
            pass


def get_project_sources_from_setup(path):
    """
    Gets the project's source(s) from `setup.py` file.
    
    Parameters
    ----------
    path : `str`
        Path to the file.
    
    Returns
    -------
    project_sources : `None | set<str>`
    error_message : `None | str`
    """
    setup_called = False
    module_packages = None
    module_name = None
    
    def setup(*, packages = None, name = None, **keyword_parameters):
        nonlocal setup_called
        nonlocal module_packages
        nonlocal module_name
        
        module_packages = packages
        module_name = name
        setup_called = True
    
    # Mock setuptools
    setup_tools_module = ModuleType('setuptools')
    setup_tools_module.setup = setup
    sys.modules['setuptools'] = setup_tools_module
    
    # Execute setup.py file
    try:
        execute_setup_file(path)
    finally:
        try:
            del sys.modules['setuptools']
        except KeyError:
            pass
    
    if not setup_called:
        return None, '`setup.py` never actually called `setup`.'
        
    return build_project_sources(module_name, module_packages), None


def get_toml_loader():
    """
    Gets toml loader and library name.
    
    Returns
    -------
    loader : `None | FunctionType`
    library_name : `None | str`
    """
    loader = None
    
    # Try toml
    library_name = 'toml'
    try:
        from toml import loads as loader
    except ImportError:
        loader = None
    else:
        return loader, library_name
    finally:
        if (loader is None):
            clean_up_toml_library(library_name)
    
    # Try tomllib
    library_name = 'tomllib'
    try:
        from tomllib import loads as loader
    except ImportError:
        loader = None
    else:
        return loader, library_name
    finally:
        if (loader is None):
            clean_up_toml_library(library_name)
    
    return None, None


def clean_up_toml_library(library_name):
    """
    Cleans up a library. Specifically used for a toml one.
    
    Parameters
    ----------
    library_name : `None | str`
        The name of the library to clean up.
    """
    # Nothing to clean up
    if library_name is None:
        return
    
    library_name_length = len(library_name)
    
    module_names = []
    
    for module_name in sys.modules.keys():
        if (
            module_name.startswith(library_name) and
            (
                (len(module_name) == library_name_length) or
                (module_name[library_name_length] == '.')
            )
        ):
            module_names.append(module_name)
    
    for module_name in module_names:
        try:
            del sys.modules[module_name]
        except KeyError:
            pass


def get_project_sources_from_toml(path):
    """
    Gets the project's source(s) from `pyproject.toml` file.
    
    Parameters
    ----------
    path : `str`
        Path to the file.
    
    Returns
    -------
    project_sources : `None | set<str>`
    error_message : `None | str`
    """
    loader, library_name = get_toml_loader()
    if loader is None:
        return None, 'Failed to read `pyproject.toml`, no `.toml` reader available.'
    
    try:
        with open(path, 'rb') as file:
            loaded = loader(file.read())
    finally:
        loader = None
        clean_up_toml_library(library_name)
    
    
    project_info = loaded.get('project', None)
    if (project_info is None) or (not isinstance(project_info, dict)):
        return None, None
    
    return build_project_sources(project_info.get('name', None), project_info.get('packages', None)), None


def get_target_path_from_parameters(parameters, index):
    """
    Gets target path from the given parameters.
    
    Parameters
    ----------
    parameters : `list<str>`
        System parameters usually.
    index : `int`
        The index to read from.
    
    Returns
    -------
    path_parameter : `str`
        The detected path parameter.
    index : `int`
        The new index to read from next time.
    """
    parameter_count = len(parameters)

    path_parameter = None
    
    if parameter_count > index:
        maybe_path = parameters[index]
        if not maybe_path.startswith('-'):
            path_parameter = maybe_path
            index += 1
    
    return path_parameter, index


def find_top_most_init_directories(path):
    """
    Gets the top-most directory with `__init__.py` or equivalent in it.
    
    Parameters
    ----------
    path : `str`
        The path to originate from.
    
    Returns
    -------
    top_most_init_directories : `None | list<str>`
        The found directory if any.
    """
    directories = []
    
    while True:
        directories.append(path)
        
        parent_directory = get_parent_directory_path(path)
        if parent_directory == path:
            break
        
        path = parent_directory
        continue
    
    chains = []
    chain = None
    
    for directory in directories:
        if not has_init(directory):
            chain = None
            continue
        
        if chain is None:
            chain = []
            chains.append(chain)
        
        chain.append(directory)
    
    if chains:
        return [chain[-1] for chain in chains]


def get_sources_from_project_source_directory(path):
    """
    Gets sources for project source directory.
    
    Parameters
    ----------
    path : `str`
        Path to the directory.
    
    Returns
    -------
    project_sources : `None | set<str>`
    error_message : `None | str`
    """
    setup_file_path = join_paths(path, 'setup.py')
    if is_file(setup_file_path):
        return get_project_sources_from_setup(setup_file_path)
    
    setup_file_path = join_paths(path, 'pyproject.toml')
    if is_file(setup_file_path):
        return get_project_sources_from_toml(setup_file_path)
    
    return None, 'Unknown setup file kind.'


def full_split_path(path):
    """
    Slits the given path removing empty parts.
    
    Parameters
    ----------
    path : `str`
        The path to split.
    
    Returns
    -------
    path_parts : `list<str>`
    """
    return [path_part for path_part in path.split(PATH_SEPARATOR) if path_part]


def get_source_and_target(parameters, index):
    """
    Looks up test source and target.
    
    Parameters
    ----------
    parameters : `list<str>`
        System parameters usually.
    index : `int`
        The index to read from.
    
    Returns
    -------
    source_directory : `str`
    sources : `None | set<str>`
    test_collection_route : `None | list<str>`
    errors : `None | list<(str, str)>`
    index : `int`
    """
    target_path, index = get_target_path_from_parameters(parameters, index)
    
    base_path = get_current_working_directory()
    if target_path is not None:
        base_path = join_paths(base_path, target_path)
    
    top_most_init_directories = find_top_most_init_directories(base_path)
    
    source_directory = None
    sources = None
    errors = None
    
    if top_most_init_directories is not None:
        # Check for setup.py-s
        for top_most_init_directory in top_most_init_directories:
            directory_path = get_parent_directory_path(top_most_init_directory)
            if not is_directory_project_source(directory_path):
                continue
            
            sources, error = get_sources_from_project_source_directory(directory_path)
            if (error is not None):
                if errors is None:
                    errors = []
                
                errors.append((directory_path, error))
            
            if (sources is not None):
                source_directory = directory_path
                break
        
        # Check init-s
        if source_directory is None:
            split = split_path(top_most_init_directories[-1])
            source_directory = split[0]
            sources = {split[1]}
    
    # Check setup.py in current.
    if is_directory_project_source(base_path):
        sources, error = get_sources_from_project_source_directory(base_path)
        if (error is not None):
            if errors is None:
                errors = []
            
            errors.append((base_path, error))
        
        if (sources is not None):
            source_directory = base_path
    
    # check current
    if source_directory is None:
        if is_file(base_path):
            split = split_path(base_path)
            source_directory = split[0]
            sources = {split_extension(split[1])[0]}
        else:
            if errors is None:
                errors = []
            
            errors.append((base_path, 'Could not identify source.'))
    
    # Resolve lookup
    if source_directory is None:
        test_collection_route = None
    else:
        test_collection_route = full_split_path(base_path[len(source_directory):])
    
    return source_directory, sources, test_collection_route, errors, index
