import sys
from io import StringIO

from ...core import assert_eq, assert_is, assert_true, mock_globals

from ..source_lookup import get_project_sources_from_toml


def test__get_project_sources_from_toml__success():
    """
    Tests whether ``get_project_sources_from_toml`` works as intended.
    
    Case: Success.
    """
    modules_count_before = len(sys.modules)
    
    directory_path = '/orin'
    file_path = '/orin/pyproject.toml'
    file_content = 'koishi'
    toml_library_name = 'toml'
    loaded = {'project': {'name': 'vampy', 'packages': ['vampy']}}
    file_paths = {
        file_path,
        '/orin/vampy/__init__.py',
    }
    
    get_toml_loader_called = False
    
    loader_called = False
    loader_called_with_content = None
    
    open_called = False
    open_called_with_path = None
    open_called_with_mode = None
    
    
    def get_toml_loader():
        nonlocal get_toml_loader_called
        nonlocal loader
        nonlocal toml_library_name
        
        get_toml_loader_called = True
        return loader, toml_library_name
    
    
    def loader(content):
        nonlocal loader_called
        nonlocal loader_called_with_content
        nonlocal loaded
        
        loader_called = True
        loader_called_with_content = content
        return loaded
    
    
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
    
    
    try:
        mocked = mock_globals(
            get_project_sources_from_toml,
            recursion = 5,
            get_toml_loader = get_toml_loader,
            is_file = is_file_mock,
            open = open_mock,
        )
        
        project_sources, error_message = mocked(directory_path, file_path)
        
        assert_eq(project_sources, {'vampy'})
        assert_is(error_message, None)
        
        assert_true(get_toml_loader_called)
        
        assert_true(loader_called)
        assert_eq(loader_called_with_content, file_content)
        
        assert_true(open_called)
        assert_eq(open_called_with_path, file_path)
        assert_eq(open_called_with_mode, 'rb')
        
        modules_count_after = len(sys.modules)
        assert_eq(modules_count_before, modules_count_after)
    
    finally:
        try:
            del sys.modules['toml']
        except KeyError:
            pass
        
        try:
            del sys.modules['tomllib']
        except KeyError:
            pass


def test__get_project_sources_from_toml__no_loader():
    """
    Tests whether ``get_project_sources_from_toml`` works as intended.
    
    Case: No toml loader.
    """
    modules_count_before = len(sys.modules)
    
    directory_path = '/orin'
    file_path = '/orin/pyproject.toml'
    get_toml_loader_called = False
    file_paths = {
        file_path,
        '/orin/vampy/__init__.py',
    }
    
    def get_toml_loader():
        nonlocal get_toml_loader_called
        
        get_toml_loader_called = True
        return None, None
    
    
    def is_file_mock(path):
        nonlocal file_paths
        return path in file_paths
    
    
    try:
        mocked = mock_globals(
            get_project_sources_from_toml,
            recursion = 5,
            get_toml_loader = get_toml_loader,
            is_file = is_file_mock,
        )
        
        project_sources, error_message = mocked(directory_path, file_path)
        
        assert_is(project_sources, None)
        assert_eq(error_message, 'Failed to read `pyproject.toml`, no `.toml` reader available.')
        
        assert_true(get_toml_loader_called)
        
        modules_count_after = len(sys.modules)
        assert_eq(modules_count_before, modules_count_after)
    
    finally:
        try:
            del sys.modules['toml']
        except KeyError:
            pass
        
        try:
            del sys.modules['tomllib']
        except KeyError:
            pass
