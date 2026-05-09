from ..source_lookup import find_top_most_init_directories
from ...core import assert_instance, assert_is, mock_globals, assert_eq


def test__find_top_most_init_directories__stops_at_root():
    """
    Tests whether ``find_top_most_init_directories`` works as intended.
    
    Case: Stops at root.
    """
    def has_init(path):
        return False
    
    
    mocked = mock_globals(
        find_top_most_init_directories,
        has_init = has_init,
    )
    
    output = mocked('/')
    assert_instance(output, str, nullable = True)
    assert_is(output, None)


def test__find_top_most_init_directories__current():
    """
    Tests whether ``find_top_most_init_directories`` works as intended.
    
    Case: Current directory is it.
    """
    resolution_map = {
        '/orin/dance': True,
        '/orin': False,
    }
    
    def has_init(path):
        nonlocal resolution_map
        return resolution_map.get(path, False)
    
    
    mocked = mock_globals(
        find_top_most_init_directories,
        has_init = has_init,
    )
        
    output = mocked('/orin/dance')
    assert_instance(output, list, nullable = True)
    assert_eq(output, ['/orin/dance'])


def test__find_top_most_init_directories__previous():
    """
    Tests whether ``find_top_most_init_directories`` works as intended.
    
    Case: A previous directory is.
    """
    resolution_map = {
        '/orin/dance/party/cat': False,
        '/orin/dance/party': False,
        '/orin/dance': True,
        '/orin': False,
    }
    
    def has_init(path):
        nonlocal resolution_map
        return resolution_map.get(path, False)
    
    
    mocked = mock_globals(
        find_top_most_init_directories,
        has_init = has_init,
    )
        
    output = mocked('/orin/dance/party/cat')
    assert_instance(output, list, nullable = True)
    assert_eq(output, ['/orin/dance'])


def test__find_top_most_init_directories__multiple():
    """
    Tests whether ``find_top_most_init_directories`` works as intended.
    
    Case: Multiple directory hit.
    """
    resolution_map = {
        '/orin/dance/party/cat/tail': True,
        '/orin/dance/party/cat': True,
        '/orin/dance/party': False,
        '/orin/dance': True,
        '/orin': False,
    }
    
    def has_init(path):
        nonlocal resolution_map
        return resolution_map.get(path, False)
    
    
    mocked = mock_globals(
        find_top_most_init_directories,
        has_init = has_init,
    )
        
    output = mocked('/orin/dance/party/cat/tail')
    assert_instance(output, list, nullable = True)
    assert_eq(output, ['/orin/dance/party/cat', '/orin/dance'])
