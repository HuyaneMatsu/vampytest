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
    
    path = '/orin/pyproject.toml'
    file_content = 'koishi'
    toml_library_name = 'toml'
    loaded = {'project': {'name': 'vampy', 'packages': ['vampy']}}
    
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
    
    
    def open(path, mode):
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
    
    try:
        mocked = mock_globals(
            get_project_sources_from_toml,
            get_toml_loader = get_toml_loader,
            open = open,
        )
        
        project_sources, error_message = mocked(path)
        
        assert_eq(project_sources, {'vampy'})
        assert_is(error_message, None)
        
        assert_true(get_toml_loader_called)
        
        assert_true(loader_called)
        assert_eq(loader_called_with_content, file_content)
        
        assert_true(open_called)
        assert_eq(open_called_with_path, path)
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


def test__get_project_sources_from_toml__no_call():
    """
    Tests whether ``get_project_sources_from_toml`` works as intended.
    
    Case: No setup call.
    """
    modules_count_before = len(sys.modules)
    
    path = '/orin/pyproject.toml'
    get_toml_loader_called = False
    
    def get_toml_loader():
        nonlocal get_toml_loader_called
        
        get_toml_loader_called = True
        return None, None
    
    try:
        mocked = mock_globals(
            get_project_sources_from_toml,
            get_toml_loader = get_toml_loader,
        )
        
        project_sources, error_message = mocked(path)
        
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
