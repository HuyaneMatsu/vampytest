__all__ = ()

import sys
from importlib.machinery import ModuleSpec, SourceFileLoader
from importlib.util import module_from_spec
from os import getcwd as get_current_working_directory, sep as PATH_SEPARATOR
from os.path import (
    dirname as get_parent_directory_path, isfile as is_file, join as join_paths, split as split_path,
    splitext as split_extension
)
from re import compile as re_compile
from shlex import split
from types import ModuleType

from scarletio.web_common import URL


PYTHON_EXTENSIONS = frozenset(('.py', '.pyd', '.pyc', '.so'))
MODULE_SCRIPT_RP = re_compile('\\w+\\s*=\\s*([\\w]+)(?:\\.[\\w\\.]*)?\\:[\\w]+')
SPACE_RP = re_compile('\\s*')
SECTION_RP = re_compile('\\[\\s*(.*?)\\s*\\]')
ASSIGNED_OPTION_RP = re_compile('\\s*(\\w+)\\s*=\\s*(.*?)\\s*')


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
    
    if is_file(join_paths(path, '.git', 'config')):
        return True
    
    return False


def add_to_project_sources(project_sources, directory_path, name):
    """
    Adds a project source.
    
    Parameters
    ----------
    project_sources : `None | set<str>`
        Project sources.
    directory_path : `str`
        Path to the directory.
    name : `str`
        The name of the project source to add.
    
    Returns
    -------
    project_sources : `None | set<str>`
    """
    if (project_sources is not None) and (name in project_sources):
        return project_sources
    
    if not has_init(join_paths(directory_path, name)):
        return project_sources
    
    if project_sources is None:
        project_sources = set()
    
    project_sources.add(name)
    return project_sources


def get_package_name_from_module_name(module_name):
    """
    Gets the package name from a module name.
    
    Parameters
    ----------
    module_name : `str`
        The name of a module.
    
    Returns
    -------
    name : `str`
        Empy string if format is invalid.
    """
    dot_index = module_name.find('.')
    if dot_index == -1:
        name = module_name
    elif dot_index > 0:
        name = module_name[:dot_index]
    else:
        name = ''
    
    return name


def get_package_name_from_module_script(module_script):
    """
    Gets the package's name from a module script.
    
    Parameters
    ----------
    module_script : `str`
        Module script.
    
    Returns
    -------
    name : `str`
        Empy string if format is invalid.
    """
    match = MODULE_SCRIPT_RP.fullmatch(module_script)
    if (match is None):
        return ''
    
    return match.group(1)


def add_to_project_sources_from_module_packages(project_sources, directory_path, module_packages):
    """
    Extends the given `project_sources` from the given `module_packages`.
    
    Parameters
    ----------
    project_sources : `None | set<str>`
        Project sources.
    directory_path : `str`
        Path to the directory.
    module_packages : `object`
        The module's packages. Preferably a list of strings.
    
    Returns
    -------
    project_sources : `None | set<str>`
    """
    if (module_packages is None) or (getattr(module_packages, '__iter__', None) is None):
        return project_sources
    
    for module_package in module_packages:
        if not isinstance(module_package, str):
            continue
        
        name = get_package_name_from_module_name(module_package)
        if not name:
            continue
        
        project_sources = add_to_project_sources(project_sources, directory_path, name)
        continue
    
    return project_sources


def add_to_project_sources_from_module_name(project_sources, directory_path, module_name):
    """
    Extends the given `project_sources` from the given `module_name`.
    
    Parameters
    ----------
    project_sources : `None | set<str>`
        Project sources.
    directory_path : `str`
        Path to the directory.
    module_packages : `object`
        The module's packages. Preferably a string.
    
    Returns
    -------
    project_sources : `None | set<str>`
    """
    if (module_name is None) or (not isinstance(module_name, str)):
        return project_sources
    
    project_sources = add_to_project_sources(project_sources, directory_path, module_name)
    return project_sources


def add_to_project_sources_from_module_scripts(project_sources, directory_path, module_scripts):
    """
    Extends the given `project_sources` from the given `module_scripts`.
    
    Parameters
    ----------
    project_sources : `None | set<str>`
        Project sources.
    directory_path : `str`
        Path to the directory.
    module_scripts : `object`
        The module's scripts. Preferably a list of strings.
    
    Returns
    -------
    project_sources : `None | set<str>`
    """
    if (module_scripts is None) or (getattr(module_scripts, '__iter__', None) is None):
        return project_sources
    
    for module_package in module_scripts:
        if not isinstance(module_package, str):
            continue
        
        name = get_package_name_from_module_script(module_package)
        if not name:
            continue
        
        project_sources = add_to_project_sources(project_sources, directory_path, name)
        continue
    
    return project_sources


def build_project_sources(directory_path, module_name, module_packages, module_scripts):
    """
    Builds the project's sources to import.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    module_name : `object`
        The module's name. Preferably a string.
    module_packages : `object`
        The module's packages. Preferably a list of strings.
    module_scripts : `object`
        The module's scripts. Preferably a list of strings.
    
    Returns
    -------
    project_sources : `None | set<str>`
    """
    project_sources = add_to_project_sources_from_module_packages(None, directory_path, module_packages)
    if (project_sources is not None):
        return project_sources
    
    project_sources = add_to_project_sources_from_module_name(None, directory_path, module_name)
    if (project_sources is not None):
        return project_sources
    
    project_sources = add_to_project_sources_from_module_scripts(None, directory_path, module_scripts)
    if (project_sources is not None):
        return project_sources
    
    # No more cases
    return None


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


def get_project_sources_from_setup(directory_path, file_path):
    """
    Gets the project's source(s) from `setup.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    file_path : `str`
        Path to the file.
    
    Returns
    -------
    project_sources : `None | set<str>`
    error_message : `None | str`
    """
    setup_called = False
    module_entry_points = None
    module_packages = None
    module_name = None
    
    def setup(*, entry_points = None, packages = None, name = None, **keyword_parameters):
        nonlocal setup_called
        nonlocal module_entry_points
        nonlocal module_packages
        nonlocal module_name
        
        module_entry_points = entry_points
        module_packages = packages
        module_name = name
        setup_called = True
    
    # Mock setuptools
    setup_tools_module = ModuleType('setuptools')
    setup_tools_module.setup = setup
    sys.modules['setuptools'] = setup_tools_module
    
    # Execute setup.py file
    try:
        execute_setup_file(file_path)
    finally:
        try:
            del sys.modules['setuptools']
        except KeyError:
            pass
    
    if not setup_called:
        return None, '`setup.py` never actually called `setup`.'
        
    return (
        build_project_sources(
            directory_path,
            module_name,
            module_packages,
            get_module_entry_points_strips(module_entry_points),
        ),
        None,
    )


def get_module_entry_points_strips(module_entry_points):
    """
    Gets the module entry point scripts.
    
    Parameters
    ----------
    module_entry_points : `object`
        Module entry points to get scripts from. Preferably `None` or `dict`.
    
    Returns
    -------
    scripts : `object`
        Preferably `None` or a `list` of `str`.
    """
    if (module_entry_points is not None) and isinstance(module_entry_points, dict):
        return module_entry_points.get('console_scripts', None)


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


def get_project_sources_from_toml(directory_path, file_path):
    """
    Gets the project's source(s) from `pyproject.toml` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    file_path : `str`
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
        with open(file_path, 'rb') as file:
            loaded = loader(file.read())
    finally:
        loader = None
        clean_up_toml_library(library_name)
    
    
    project_info = loaded.get('project', None)
    if (project_info is None) or (not isinstance(project_info, dict)):
        return None, None
    
    return (
        build_project_sources(
            directory_path,
            project_info.get('name', None),
            project_info.get('packages', None),
            project_info.get('project.scripts', None),
        ),
        None,
    )


def parse_git_config_file_content(content):
    """
    Parses a git config file's content.
    
    Parameters
    ----------
    content : `str`
        Content to parse.
    
    Returns
    -------
    sections : `dict<str, ... | str>`
    """
    sections = {}
    section_path_parts = []
    
    for line in content.splitlines():
        if SPACE_RP.fullmatch(line) is not None:
            continue
        
        match = SECTION_RP.fullmatch(line)
        if (match is not None):
            section_path_parts = split(match.group(1))
            continue
        
        match = ASSIGNED_OPTION_RP.fullmatch(line)
        if match is None:
            continue
        
        key, value = match.groups()
        
        sub_section = sections
        for part in section_path_parts:
            try:
                section = sub_section[part]
            except KeyError:
                section = {}
                sub_section[part] = section
            
            sub_section = section
        
        sub_section[key] = value
    
    return sections


def try_get_nested(sections, path_parts):
    """
    Tries to get a nested value from the given `sections` value.
    
    Parameters
    ----------
    sections : `dict<str, ... | str>`
        Sections to get from.
    path_parts : `tuple<str>`
        Path to query for.
    
    Returns
    -------
    value : `None | dict<str, ...> | str`
    """
    for path_part in path_parts:
        if not isinstance(sections, dict):
            return None
        
        try:
            sections = sections[path_part]
        except KeyError:
            return None
    
    return sections


def get_project_sources_from_git(directory_path, file_path):
    """
    Gets the project's source(s) from `.git/config` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    file_path : `str`
        Path to the file.
    
    Returns
    -------
    project_sources : `None | set<str>`
    error_message : `None | str`
    """
    with open(file_path, 'r') as file:
        sections = parse_git_config_file_content(file.read())
    
    url = try_get_nested(sections, ('remote', 'origin', 'url'))
    if (url is None) or (not isinstance(url, str)):
        return None, 'Failed to get remote origin url.'
    
    try:
        url = URL(url)
    except ValueError as exception:
        return None, f'Remote origin url invalid; url = {url!r} error = {exception!s}'
    
    name = url.name
    if not name:
        return None, f'Remote origin url has no name; url = {url!r}'
    
    return (
        add_to_project_sources(None, directory_path, name),
        None
    )


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


def get_sources_from_project_source_directory(directory_path):
    """
    Gets sources for project source directory.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    
    Returns
    -------
    project_sources : `None | set<str>`
    error_message : `None | str`
    """
    file_path = join_paths(directory_path, 'setup.py')
    if is_file(file_path):
        return get_project_sources_from_setup(directory_path, file_path)
    
    file_path = join_paths(directory_path, 'pyproject.toml')
    if is_file(file_path):
        return get_project_sources_from_toml(directory_path, file_path)
    
    file_path = join_paths(directory_path, '.git', 'config')
    if is_file(file_path):
        return get_project_sources_from_git(directory_path, file_path)
    
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
