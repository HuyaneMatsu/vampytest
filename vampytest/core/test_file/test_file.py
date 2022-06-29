__all__ = ('TestFile', )

import sys

from ..exceptions import TestLoadingError
from ..utils import get_short_path_repr
from ..test_case import TestCase
from ..wrappers import WrapperBase

from .test_file_load_failure import TestFileLoadFailure

from scarletio import RichAttributeErrorBaseType


def is_test_name(name):
    """
    Returns whether the given name should be collected as a test.
    
    Parameters
    ----------
    name : `str`
        The test's name.
    
    Returns
    -------
    is_test_name : `bool`
    """
    if name == 'test':
        return True
    
    if name.startswith('test_'):
        return True
    
    return False


def is_test(name, value):
    """
    Returns whether the given name - value pair refers to a test.
    
    Parameters
    ----------
    name : `str`
        The name of a a variable.
    value : `Any`
        The variable's value.
    
    Returns
    -------
    is_test : `bool`
    """
    if not is_test_name(name):
        return False
    
    if isinstance(value, WrapperBase):
        return value.has_bound_test()
    
    return callable(value)
    

class TestFile(RichAttributeErrorBaseType):
    """
    Describes a test file.
    
    Attributes
    ----------
    import_route : `str`
        Import route from the base path to import the file from.
    module : `None`, `ModuleType`
        The module of the test file. Only set when the first call is made to it.
    path : `str`
        Absolute path to the file.
    tests : `None`, `list` of ``TestCase``
        The collected tests from the file if any. These tests are on collected after calling ``.get_tests`` for
        the first time.
    """
    __slots__ = ('import_route', 'module', 'path', 'tests')
    
    def __new__(cls, path, path_parts):
        """
        Creates an new test file.
        
        Parameters
        ----------
        path : `str`
            Absolute path to the file.
        path_parts: `list` of `str`
            Path parts from base path to the file.
        """
        if path_parts:
            last_path_part = path_parts[-1]
            if last_path_part.endswith('.py'):
                path_parts[-1] = last_path_part[:-len('.py')]
        
        import_route = '.'.join(path_parts)
        
        self = object.__new__(cls)
        self.module = None
        self.import_route = import_route
        self.path = path
        self.tests = None
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two test files are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.path == other.path
    
    
    def __hash__(self):
        """Returns the hash value of the test file."""
        return hash(self.path)
    
    
    def __repr__(self):
        """Returns the representation of a test file."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' path=')
        repr_parts.append(get_short_path_repr(self.path))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_module(self):
        """
        Gets the module of the test file.
        
        Returns
        -------
        module : `ModuleType`
        
        Raises
        ------
        TestLoadingError
            Loading test file failed.
        """
        module = self.module
        if (module is None):
            module = self._get_module()
        
        return module
    
    
    def _get_module(self):
        """
        Loads the test the's module.
        
        Called by ``.get_module` when first time getting the module.
        
        Returns
        -------
        module : `ModuleType`
        
        Raises
        ------
        TestLoadingError
            Loading test file failed.
        """
        import_route = self.import_route
        
        try:
            __import__(import_route)
        except BaseException as err:
            raise TestLoadingError(err) from None
        
        module = sys.modules[import_route]
        self.module = module
        return module
    
    
    def try_load_tests(self):
        """
        Loads the file's tests.
        
        If loading fails, returns an object representing its failure.
        
        Returns
        -------
        load_failure : `None`, ``TestFileLoadFailure``
        """
        try:
            self.get_tests()
        except TestLoadingError as err:
            return TestFileLoadFailure(self, err)
    
    
    def get_tests(self):
        """
        Collects the tests in the test file.
        
        Returns
        -------
        tests : `list` of ``TestCase``
        
        Raises
        ------
        TestLoadingError
            Loading test file failed.
        """
        tests = self.tests
        if (tests is None):
            tests = self._get_tests()
        
        return tests
    
    
    def _get_tests(self):
        """
        Collects the tests from the test file.
        
        Called by ``._get_tests`` for the first time the tests are get.
        
        Returns
        -------
        tests : `list` of ``TestCase``
        
        Raises
        ------
        TestLoadingError
            Loading test file failed.
        """
        module = self.get_module()
        
        tests = []
        
        import_route = self.import_route
        
        for name, value in module.__dict__.items():
            if is_test(name, value):
                tests.append(TestCase(import_route, name, value))
        
        self.tests = tests
        return tests
