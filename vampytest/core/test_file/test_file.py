__all__ = ('TestFile', )

import sys

from ..utils import get_short_path_repr
from ..test_case import TestCase
from ..wrappers import WrapperBase

from .load_failure import TestFileLoadFailure

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


def _test_case_sort_key(test_case):
    """
    Sort key for test cases.
    
    Parameters
    ----------
    test_case : ``TestKey``
        Test case to get it's sort keys.
    
    Returns
    -------
    sort_key : `str`
    """
    return test_case.name


class TestFile(RichAttributeErrorBaseType):
    """
    Describes a test file.
    
    Attributes
    ----------
    _load_failure : `None`, ``TestFileLoadFailure``
        If loading the test file fails, this attribute is set to details about the occurred exception.
    _module : `None`, `ModuleType`
        The module of the test file. Only set when the first call is made to it.
    _result_groups : `None`, `list` of ``ResultGroup``
        Results of already ran tests.
    _test_cases : `None`, `list` of ``TestCase``
        The collected test_cases from the file if any. These test_cases are on collected after calling ``.get_test_cases`` for
        the first time.
    import_route : `str`
        Import route from the base path to import the file from.
    path : `str`
        Absolute path to the file.
    
    Utility Methods
    ---------------
    - Checks & State
    
        - ``.is_loaded_with_success``
        - ``.is_loaded_with_failure``
        - ``.get_load_failure``
    
    - Iterators
    
        - ``.iter_result_groups``
        - ``.iter_passed_result_groups``
        - ``.iter_skipped_result_groups``
        - ``.iter_failed_result_groups``
    
    - Counters
    
        - ``.get_test_case_count``
        - ``.get_ran_test_count``
        - ``.get_passed_test_count``
        - ``.get_skipped_test_count``
        - ``.get_failed_test_count``
    
    - Internal
        
        - ``.get_module``
        - ``.try_load_test_cases``
        - ``.get_test_cases``
        - ``.iter_test_cases``
        - ``.iter_invoke_test_cases``
    """
    __slots__ = ('_load_failure', '_module', '_result_groups', '_test_cases', 'import_route', 'path')
    
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
        self._load_failure = None
        self._module = None
        self._result_groups = None
        self._test_cases = None
        self.import_route = import_route
        self.path = path
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
        module : `None`, `ModuleType`
        
        Raises
        ------
        TestLoadingError
            Loading test file failed.
        """
        if self._load_failure is not None:
            return None
        
        if self._try_load_module():
            return self._module
        
        return None
    
    
    def _try_load_module(self):
        """
        Tries to load the test file's module.
        
        Called by ``.get_module` when first time getting the module.
        
        Returns
        -------
        loaded : `bool`
            Whether the module loaded.
        """
        import_route = self.import_route
        
        try:
            __import__(import_route)
        except BaseException as err:
            self._load_failure = TestFileLoadFailure(self, err)
            return False
        
        module = sys.modules[import_route]
        self._module = module
        return True
    
    
    def try_load_test_cases(self):
        """
        Loads the file's test_cases.
        
        If loading fails, returns an object representing its failure.
        
        Returns
        -------
        loaded : `bool`
            Whether the tests loaded.
        """
        module = self.get_module()
        if module is None:
            return False
        
        test_cases = []
        
        import_route = self.import_route
        
        for name, value in module.__dict__.items():
            if is_test(name, value):
                test_cases.append(TestCase(import_route, name, value))
        
        test_cases.sort(key=_test_case_sort_key)
        
        self._test_cases = test_cases
        return True
    
    
    def is_loaded_with_success(self):
        """
        Returns whether the tests loaded.
        
        Returns
        -------
        is_loaded_with_success : `bool`
        """
        return self._test_cases is not None
    
    
    def is_loaded_with_failure(self):
        """
        Returns whether loading the test file failed.
        
        Returns
        -------
        is_loaded_with_failure : `bool`
        """
        return self._load_failure is not None
    
    
    def get_load_failure(self):
        """
        Returns the loading failure representing the exception occurred when loading the test file.
        
        Returns
        -------
        load_failure : `None`, ``TestFileLoadFailure``
        """
        return self._load_failure
    
    
    def get_test_cases(self):
        """
        Collects the test cases in the test file.
        
        Returns
        -------
        test_cases : `list` of ``TestCase``
        
        Raises
        ------
        TestLoadingError
            Loading test file failed.
        """
        test_cases = self._test_cases
        if (test_cases is None):
            test_cases = []
        
        else:
            test_cases = test_cases.copy()
        
        return test_cases
    
    
    def iter_test_cases(self):
        """
        Iterates over the test_cases of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        test : ``TestCase``
        """
        test_cases = self._test_cases
        if (test_cases is not None):
            yield from test_cases
    
    
    def iter_invoke_test_cases(self, environment_manager):
        """
        Iterates over the test cases of the file and invokes them. Yields the test cases' results.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        environment_manager : ``EnvironmentManager``
            Testing environment manager.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        result_groups = self._result_groups
        if (result_groups is not None):
            return (yield from result_groups)
        
        for test_case in self.iter_test_cases():
            result_group = test_case.invoke(environment_manager)
            
            if (result_groups is None):
                result_groups = []
                self._result_groups = result_groups
            
            result_groups.append(result_group)
            
            yield result_group
    
    
    def iter_result_groups(self):
        """
        Iterates over the result groups of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        result_groups = self._result_groups
        if (result_groups is not None):
            yield from result_groups
        
    
    def get_test_case_count(self):
        """
        Returns how much test cases are in the test file collected.
        
        Returns
        -------
        test_case_count : `int`
        """
        test_cases = self._test_cases
        if (test_cases is None):
            test_count = 0
        else:
            test_count = len(test_cases)
        
        return test_count
    
    
    def get_ran_test_count(self):
        """
        Returns how much tests already ran of the file.
        
        Returns
        -------
        ran_test_count : `int`
        """
        result_groups = self._result_groups
        if (result_groups is None):
            ran_test_count = 0
        else:
            ran_test_count = len(result_groups)
        
        return ran_test_count
    
    
    def iter_passed_result_groups(self):
        """
        Iterates over the passed result groups of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        for result_group in self.iter_result_groups():
            if result_group.is_passed():
                yield result_group
    
    
    def iter_skipped_result_groups(self):
        """
        Iterates over the skipped result groups of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        for result_group in self.iter_result_groups():
            if result_group.is_skipped():
                yield result_group
    
    
    def iter_failed_result_groups(self):
        """
        Iterates over the failed result groups of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        for result_group in self.iter_result_groups():
            if result_group.is_failed():
                yield result_group
    
    
    def get_passed_test_count(self):
        """
        Returns how much test passed.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(result_group.is_passed() for result_group in self.iter_result_groups())
    
    
    def get_skipped_test_count(self):
        """
        Returns how much test was skipped.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(result_group.is_skipped() for result_group in self.iter_result_groups())
    
    
    def get_failed_test_count(self):
        """
        Returns how much test failed.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(result_group.is_failed() for result_group in self.iter_result_groups())
