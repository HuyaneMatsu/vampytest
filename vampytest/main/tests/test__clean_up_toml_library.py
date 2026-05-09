import sys

from ...core import assert_eq, assert_not_in

from ..source_lookup import clean_up_toml_library


def test__clean_up_toml_library__none():
    """
    Tests whether ``clean_up_toml_library`` works as intended.
    
    Case: Nothing to clean up.
    """
    modules_count_before = len(sys.modules)
    clean_up_toml_library(None)
    modules_count_after = len(sys.modules)
    
    assert_eq(modules_count_before, modules_count_after)


def test__clean_up_toml_library__something():
    """
    Tests whether ``clean_up_toml_library`` works as intended.
    
    Case: Something to clean up.
    """
    modules_count_before = len(sys.modules)
    
    try:
        sys.modules['toml'] = None
        sys.modules['toml.utils'] = None
        
        clean_up_toml_library('toml')
        modules_count_after = len(sys.modules)
        
        assert_eq(modules_count_before, modules_count_after)
        assert_not_in('toml', sys.modules.keys())
        assert_not_in('toml.utils', sys.modules.keys())
        
    finally:
        try:
            del sys.modules['toml']
        except KeyError:
            pass
        
        try:
            del sys.modules['toml.utils']
        except KeyError:
            pass
