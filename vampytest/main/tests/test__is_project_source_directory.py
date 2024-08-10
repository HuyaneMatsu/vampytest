from os.path import join as join_paths

from ...core import assert_eq, assert_instance, mock_globals

from ..source_lookup import is_directory_project_source


def test__is_directory_project_source__setup():
    """
    Tests whether ``is_directory_project_source`` works as intended.
    
    Case: has `setup.py`.
    """
    directory_path = '/orin'
    
    def is_file(path):
        nonlocal directory_path    
        return path == join_paths(directory_path, 'setup.py')
    
    
    def is_directory(path):
        return False
    
    
    mocked = mock_globals(
        is_directory_project_source,
        is_directory = is_directory,
        is_file = is_file,
    )
    
    output = mocked(directory_path)
    
    assert_instance(output, bool)
    assert_eq(output, True)


def test__is_directory_project_source__pyproject():
    """
    Tests whether ``is_directory_project_source`` works as intended.
    
    Case: has `pyproject.toml`.
    """
    directory_path = '/orin'
    
    
    def is_file(path):
        nonlocal directory_path
        return path == join_paths(directory_path, 'pyproject.toml')
    
    
    def is_directory(path):
        return False
    
    
    mocked = mock_globals(
        is_directory_project_source,
        is_directory = is_directory,
        is_file = is_file,
    )
    
    output = mocked(directory_path)
    
    assert_instance(output, bool)
    assert_eq(output, True)


def test__is_directory_project_source__git():
    """
    Tests whether ``is_directory_project_source`` works as intended.
    
    Case: has `.git`.
    """
    directory_path = '/orin'
    
    
    def is_file(path):
        nonlocal directory_path
        return path == join_paths(directory_path, '.git', 'config')
    
    
    def is_directory(path):
        return False
    
    
    mocked = mock_globals(
        is_directory_project_source,
        is_directory = is_directory,
        is_file = is_file,
    )
    
    output = mocked(directory_path)
    
    assert_instance(output, bool)
    assert_eq(output, True)


def test__is_directory_project_source__failure():
    """
    Tests whether ``is_directory_project_source`` works as intended.
    
    Case: has `pyproject.toml`.
    """
    directory_path = '/orin'
    
    
    def is_file(path):
        return False
    
    
    def is_directory(path):
        return False
    
    
    mocked = mock_globals(
        is_directory_project_source,
        is_directory = is_directory,
        is_file = is_file,
    )
    
    output = mocked(directory_path)
    
    assert_instance(output, bool)
    assert_eq(output, False)
