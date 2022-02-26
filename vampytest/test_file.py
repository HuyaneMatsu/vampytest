__all__ = ('TestFile', )

from .utils import get_short_path_repr
from .test_case import TestCase
from .wrappers import WrapperBase


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
    

class TestFile:
    """
    Describes a test file.
    
    Attributes
    ----------
    path : `str`
        Absolute path to the file.
    tests : `None`, `list` of ``TestCase``
        The collected tests from the file if any. These tests are on collected after calling ``.get_tests`` for
        the first time.
    module : `None`, `ModuleType`
        The module of the test file. Only set when the first call is made to it.
    """
    __slots__ = ('path', 'tests')
    
    def __new__(cls, path):
        """
        Creates an new test file.
        
        Parameters
        ----------
        path : `str`
            Absolute path to the file.
        """
        self = object.__new__(cls)
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
        """
        # TODO
        raise NotImplementedError
    
    
    def get_tests(self):
        """
        Collects the tests in the test file.
        
        Returns
        -------
        tests : `list` of ``TestCase``
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
        """
        module = self.get_module()
        
        tests = []
        
        for name, value in module.__dir__.items():
            if is_test(name, value):
                tests.append(TestCase(name, value))
        
        self.tests = tests
        return tests
