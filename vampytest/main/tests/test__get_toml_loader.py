import sys
from types import ModuleType

from ...core import assert_in, assert_is, assert_not_in

from ..source_lookup import get_toml_loader


def test__get_toml_loader__fail():
    """
    Tests whether ``get_toml_loader`` works as intended.
    
    Case: Finding `without loader.
    """
    module_toml = ModuleType('toml')
    module_tomllib = ModuleType('tomllib')
    
    try:
        sys.modules['toml'] = module_toml
        sys.modules['tomllib'] = module_tomllib
        
        loader, library_name = get_toml_loader()
        
        assert_is(loader, None)
        assert_is(library_name, None)
        
        assert_not_in('toml', sys.modules)
        assert_not_in('tomllib', sys.modules)
    
    finally:
        try:
            del sys.modules['toml']
        except KeyError:
            pass
        try:
            del sys.modules['tomllib']
        except KeyError:
            pass


def test__get_toml_loader__success_toml():
    """
    Tests whether ``get_toml_loader`` works as intended.
    
    Case: Finding `toml`.
    """
    toml_loader = lambda s: {}
    module_toml = ModuleType('toml')
    module_toml.loads = toml_loader
    module_tomllib = ModuleType('tomllib')
    
    try:
        sys.modules['toml'] = module_toml
        sys.modules['tomllib'] = module_tomllib
        
        loader, library_name = get_toml_loader()
        
        assert_is(loader, toml_loader)
        assert_is(library_name, 'toml')
        
        assert_in('toml', sys.modules)
        # we check for toml first, so ignore if tomllib is in sys.modules
        # assert_not_in('tomllib', sys.modules)
    
    finally:
        try:
            del sys.modules['toml']
        except KeyError:
            pass
        try:
            del sys.modules['tomllib']
        except KeyError:
            pass


def test__get_toml_loader__success_tomllib():
    """
    Tests whether ``get_toml_loader`` works as intended.
    
    Case: Finding `tomllib`.
    """
    toml_loader = lambda s: {}
    module_toml = ModuleType('toml')
    module_tomllib = ModuleType('tomllib')
    module_tomllib.loads = toml_loader
    
    try:
        sys.modules['toml'] = module_toml
        sys.modules['tomllib'] = module_tomllib
        
        loader, library_name = get_toml_loader()
        
        assert_is(loader, toml_loader)
        assert_is(library_name, 'tomllib')
        
        assert_not_in('toml', sys.modules)
        assert_in('tomllib', sys.modules)
    
    finally:
        try:
            del sys.modules['toml']
        except KeyError:
            pass
        try:
            del sys.modules['tomllib']
        except KeyError:
            pass
