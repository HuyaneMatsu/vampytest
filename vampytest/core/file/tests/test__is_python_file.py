from ...assertions import assert_eq, assert_instance
from ...mocking import mock_globals

from ..file_system_entry import is_python_file


def test__is_python_file__hit_py_file():
    """
    Tests whether ``is_python_file`` works as intended.
    
    Case: hit.
    """
    path = '/orin/cat.py'
    
    def is_file(checked_path):
        nonlocal path
        return checked_path == path
    
    mocked = mock_globals(
        is_python_file,
        is_file = is_file,
    )
        
    output = mocked(path)
    assert_instance(output, str, nullable = True)
    assert_eq(output, path)
    

def test__is_python_file__miss_py_file():
    """
    Tests whether ``is_python_file`` works as intended.
    
    Case: missing.
    """
    path = '/orin/cat.py'
    
    def is_file(checked_path):
        nonlocal path
        # We should never look up this file. Since it has double `.py`
        return checked_path == path + '.py'
    
    mocked = mock_globals(
        is_python_file,
        is_file = is_file,
    )
    
    output = mocked(path)
    assert_instance(output, str, nullable = True)
    assert_eq(output, None)


def test__is_python_file__hit_with_added_extension():
    """
    Tests whether ``is_python_file`` works as intended.
    
    Case: hitting with added extension.
    """
    path = '/orin/cat'
    
    def is_file(checked_path):
        nonlocal path
        return checked_path == path + '.py'
    
    mocked = mock_globals(
        is_python_file,
        is_file = is_file,
    )
        
    output = mocked(path)
    assert_instance(output, str, nullable = True)
    assert_eq(output, path + '.py')
