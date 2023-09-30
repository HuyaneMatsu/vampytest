from os.path import join as join_paths

from ...core import assert_eq, assert_false, assert_instance, assert_is, assert_true, mock_globals

from ..source_lookup import get_sources_from_project_source_directory


def test__get_sources_from_project_source_directory__setup():
    """
    Tests whether ``get_sources_from_project_source_directory`` works as intended.
    
    Case: setup.
    """
    path = '/orin'
    
    sources = {'vampy'}
    error = 'koishi'
    
    setup_called = False
    toml_called = False
    
    
    def is_file(checked_path):
        nonlocal path
        return checked_path == join_paths(path, 'setup.py')
    
    
    def get_project_sources_from_setup(file_path):
        nonlocal setup_called
        nonlocal sources
        nonlocal error
        setup_called = True
        return sources, error
    
    
    def get_project_sources_from_toml(file_path):
        nonlocal toml_called
        toml_called = True
        return None, None
        
    mocked = mock_globals(
        get_sources_from_project_source_directory,
        is_file = is_file,
        get_project_sources_from_setup = get_project_sources_from_setup,
        get_project_sources_from_toml = get_project_sources_from_toml,
    )
    
    output_sources, output_error = mocked(path)
    
    assert_true(setup_called)
    assert_false(toml_called)
    
    assert_eq(sources, output_sources)
    assert_eq(error, output_error)


def test__get_sources_from_project_source_directory__toml():
    """
    Tests whether ``get_sources_from_project_source_directory`` works as intended.
    
    Case: toml.
    """
    path = '/orin'
    
    sources = {'vampy'}
    error = 'koishi'
    
    setup_called = False
    toml_called = False
    
    
    def is_file(checked_path):
        nonlocal path
        return checked_path == join_paths(path, 'pyproject.toml')
    
    
    def get_project_sources_from_setup(file_path):
        nonlocal setup_called
        setup_called = True
        return None, None
    
    
    def get_project_sources_from_toml(file_path):
        nonlocal toml_called
        nonlocal sources
        nonlocal error
        toml_called = True
        return sources, error
        
    mocked = mock_globals(
        get_sources_from_project_source_directory,
        is_file = is_file,
        get_project_sources_from_setup = get_project_sources_from_setup,
        get_project_sources_from_toml = get_project_sources_from_toml,
    )
    
    output_sources, output_error = mocked(path)
    
    assert_false(setup_called)
    assert_true(toml_called)
    
    assert_eq(sources, output_sources)
    assert_eq(error, output_error)


def test__get_sources_from_project_source_directory__unknown():
    """
    Tests whether ``get_sources_from_project_source_directory`` works as intended.
    
    Case: toml.
    """
    path = '/orin'
    
    setup_called = False
    toml_called = False
    
    
    def is_file(checked_path):
        return False
    
    
    def get_project_sources_from_setup(file_path):
        nonlocal setup_called
        setup_called = True
        return None, None
    
    
    def get_project_sources_from_toml(file_path):
        nonlocal toml_called
        toml_called = True
        return None, None
        
    mocked = mock_globals(
        get_sources_from_project_source_directory,
        is_file = is_file,
        get_project_sources_from_setup = get_project_sources_from_setup,
        get_project_sources_from_toml = get_project_sources_from_toml,
    )
    
    output_sources, output_error = mocked(path)
    
    assert_false(setup_called)
    assert_false(toml_called)
    
    assert_is(output_sources, None)
    assert_instance(output_error, str)
