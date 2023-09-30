import sys

from ...core import assert_eq, assert_is, assert_true, mock_globals

from ..source_lookup import get_project_sources_from_setup


def test__get_project_sources_from_setup__success():
    """
    Tests whether ``get_project_sources_from_setup`` works as intended.
    
    Case: Success.
    """
    modules_count_before = len(sys.modules)
    
    path = '/orin/setup.py'
    execute_called = False
    execute_called_with_path = None
    
    def execute_setup_file(path):
        nonlocal execute_called
        nonlocal execute_called_with_path
        
        execute_called = True
        execute_called_with_path = path
        
        import setuptools
        setuptools.setup(name = 'vampy', packages = ['vampy'])
    
    try:
        mocked = mock_globals(
            get_project_sources_from_setup,
            execute_setup_file = execute_setup_file,
        )
        
        project_sources, error_message = mocked(path)
        
        assert_eq(project_sources, {'vampy'})
        assert_is(error_message, None)
        
        assert_true(execute_called)
        assert_eq(execute_called_with_path, path)
        
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
    
    path = '/orin/setup.py'
    execute_called = False
    execute_called_with_path = None
    
    def execute_setup_file(path):
        nonlocal execute_called
        nonlocal execute_called_with_path
        
        execute_called = True
        execute_called_with_path = path
    
    try:
        mocked = mock_globals(
            get_project_sources_from_setup,
            execute_setup_file = execute_setup_file,
        )
        
        project_sources, error_message = mocked(path)
        
        assert_is(project_sources, None)
        assert_eq(error_message, '`setup.py` never actually called `setup`.')
        
        assert_true(execute_called)
        assert_eq(execute_called_with_path, path)
        
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
