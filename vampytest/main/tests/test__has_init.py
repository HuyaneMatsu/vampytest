from os.path import join as join_paths

from ...core import assert_eq, assert_in, assert_instance, mock_globals

from ..source_lookup import has_init


def test__has_init__false():
    """
    Tests whether ``has_init`` is works as intended.
    
    Case: Does not exist.
    """
    path = '/orin'
    
    is_file_called_with = set()
    
    def is_file(checked_path):
        nonlocal is_file_called_with
        is_file_called_with.add(checked_path)
        return False
    
    mocked = mock_globals(
        has_init,
        is_file = is_file,
    )
    
    output = mocked(path)
    assert_instance(output, bool)
    assert_eq(output, False)
    
    assert_in(join_paths(path, '__init__.py'), is_file_called_with)


def test__has_init__true():
    """
    Tests whether ``has_init`` works as intended.
    
    Case: exists.
    """
    path = '/orin'
    
    def is_file(checked_path):
        return checked_path.endswith('__init__.py')
    
    mocked = mock_globals(
        has_init,
        is_file = is_file,
    )
    
    output = mocked(path)
    assert_instance(output, bool)
    assert_eq(output, True)
