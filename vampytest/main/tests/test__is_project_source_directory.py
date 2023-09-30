from os.path import join as join_paths

from ...core import assert_eq, assert_instance, mock_globals

from ..source_lookup import is_directory_project_source


def test__is_directory_project_source__setup():
    """
    Tests whether ``is_directory_project_source`` works as intended.
    
    Case: has `setup.py`.
    """
    path = '/orin'
    
    def is_file(checked_path):
        nonlocal path
        
        return checked_path == join_paths(path, 'setup.py')
    
    
    mocked = mock_globals(
        is_directory_project_source,
        is_file = is_file,
    )
    
    output = mocked(path)
    
    assert_instance(output, bool)
    assert_eq(output, True)


def test__is_directory_project_source__pyproject():
    """
    Tests whether ``is_directory_project_source`` works as intended.
    
    Case: has `pyproject.toml`.
    """
    path = '/orin'
    
    def is_file(checked_path):
        nonlocal path
        
        return checked_path == join_paths(path, 'pyproject.toml')
    
    
    mocked = mock_globals(
        is_directory_project_source,
        is_file = is_file,
    )
    
    output = mocked(path)
    
    assert_instance(output, bool)
    assert_eq(output, True)


def test__is_directory_project_source__failure():
    """
    Tests whether ``is_directory_project_source`` works as intended.
    
    Case: has `pyproject.toml`.
    """
    path = '/orin'
    
    def is_file(checked_path):
        return False
    
    mocked = mock_globals(
        is_directory_project_source,
        is_file = is_file,
    )
    
    output = mocked(path)
    
    assert_instance(output, bool)
    assert_eq(output, False)
