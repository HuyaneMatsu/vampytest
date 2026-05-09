from io import StringIO

from ...core import assert_eq, assert_is, assert_true, mock_globals

from ..source_lookup import get_project_sources_from_git


def test__get_project_sources_from_git__success():
    """
    Tests whether ``get_project_sources_from_git`` works as intended.
    
    Case: Success.
    """
    directory_path = '/orin'
    file_path = '/orin/.git/config'
    file_content = '[remote "origin"]\n\turl = https://orindance.party/vampy\n'
    file_paths = {
        file_path,
        '/orin/vampy/__init__.py',
    }
    
    open_called = False
    open_called_with_path = None
    open_called_with_mode = None
    
    
    def open_mock(path, mode):
        nonlocal open_called
        nonlocal open_called_with_path
        nonlocal open_called_with_mode
        nonlocal file_content
        
        open_called = True
        open_called_with_path = path
        open_called_with_mode = mode
        
        io = StringIO()
        io.write(file_content)
        io.seek(0)
        return io
    
    
    def is_file_mock(path):
        nonlocal file_paths
        return path in file_paths
    
    
    mocked = mock_globals(
        get_project_sources_from_git,
        recursion = 5,
        is_file = is_file_mock,
        open = open_mock,
    )
    
    project_sources, error_message = mocked(directory_path, file_path)
    
    assert_eq(project_sources, {'vampy'})
    assert_is(error_message, None)
    
    assert_true(open_called)
    assert_eq(open_called_with_path, file_path)
    assert_eq(open_called_with_mode, 'r')


def test__get_project_sources_from_git__no_remote_origin_url():
    """
    Tests whether ``get_project_sources_from_git`` works as intended.
    
    Case: No remote origin url.
    """
    directory_path = '/orin'
    file_path = '/orin/.git/config'
    file_content = '[remote "main"]\n\turl = https://orindance.party/vampy\n'
    file_paths = {
        file_path,
        '/orin/vampy/__init__.py',
    }
    
    open_called = False
    open_called_with_path = None
    open_called_with_mode = None
    
    
    def open_mock(path, mode):
        nonlocal open_called
        nonlocal open_called_with_path
        nonlocal open_called_with_mode
        nonlocal file_content
        
        open_called = True
        open_called_with_path = path
        open_called_with_mode = mode
        
        io = StringIO()
        io.write(file_content)
        io.seek(0)
        return io
    
    
    def is_file_mock(path):
        nonlocal file_paths
        return path in file_paths
    
    mocked = mock_globals(
        get_project_sources_from_git,
        recursion = 3,
        is_file = is_file_mock,
        open = open_mock,
    )
    
    project_sources, error_message = mocked(directory_path, file_path)
    
    assert_is(project_sources, None)
    assert_eq(error_message, 'Failed to get remote origin url.')
    
    
    assert_true(open_called)
    assert_eq(open_called_with_path, file_path)
    assert_eq(open_called_with_mode, 'r')
