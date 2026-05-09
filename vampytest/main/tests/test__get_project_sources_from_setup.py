import sys

from ...core import assert_eq, assert_is, assert_true, mock_globals

from ..source_lookup import get_project_sources_from_setup


def test__get_project_sources_from_setup__success():
    """
    Tests whether ``get_project_sources_from_setup`` works as intended.
    
    Case: Success.
    """
    modules_count_before = len(sys.modules)
    
    directory_path = '/orin'
    file_path = '/orin/setup.py'
    execute_called = False
    execute_called_with_path = None
    file_paths = {
        file_path,
        '/orin/vampy/__init__.py',
    }
    
    def execute_setup_file(path):
        nonlocal execute_called
        nonlocal execute_called_with_path
        
        execute_called = True
        execute_called_with_path = path
        
        import setuptools
        setuptools.setup(name = 'vampy', packages = ['vampy'])
    
    
    def is_file_mock(path):
        nonlocal file_paths
        return path in file_paths
    
    
    try:
        mocked = mock_globals(
            get_project_sources_from_setup,
            recursion = 5,
            execute_setup_file = execute_setup_file,
            is_file = is_file_mock,
        )
        
        project_sources, error_message = mocked(directory_path, file_path)
        
        assert_eq(project_sources, {'vampy'})
        assert_is(error_message, None)
        
        assert_true(execute_called)
        assert_eq(execute_called_with_path, file_path)
        
        modules_count_after = len(sys.modules)
        assert_eq(modules_count_before, modules_count_after)
    
    finally:
        try:
            del sys.modules['setuptools']
        except KeyError:
            pass
        
        try:
            del sys.modules['setup']
        except KeyError:
            pass


def test__get_project_sources_from_setup__no_call():
    """
    Tests whether ``get_project_sources_from_setup`` works as intended.
    
    Case: No setup call.
    """
    modules_count_before = len(sys.modules)
    
    directory_path = '/orin'
    file_path = '/orin/setup.py'
    execute_called = False
    execute_called_with_path = None
    file_paths = {
        file_path,
        '/orin/vampy/__init__.py',
    }
    
    def execute_setup_file(path):
        nonlocal execute_called
        nonlocal execute_called_with_path
        
        execute_called = True
        execute_called_with_path = path
    
    
    def is_file_mock(path):
        nonlocal file_paths
        return path in file_paths
    
    
    try:
        mocked = mock_globals(
            get_project_sources_from_setup,
            recursion = 5,
            is_file = is_file_mock,
            execute_setup_file = execute_setup_file,
        )
        
        project_sources, error_message = mocked(directory_path, file_path)
        
        assert_is(project_sources, None)
        assert_eq(error_message, '`setup.py` never actually called `setup`.')
        
        assert_true(execute_called)
        assert_eq(execute_called_with_path, file_path)
        
        modules_count_after = len(sys.modules)
        assert_eq(modules_count_before, modules_count_after)
    
    finally:
        try:
            del sys.modules['setuptools']
        except KeyError:
            pass
        
        try:
            del sys.modules['setup']
        except KeyError:
            pass
