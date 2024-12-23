__all__ = ('TestFile', )

from sys import modules
from types import FunctionType

from scarletio import RichAttributeErrorBaseType

from ..environment import apply_environments_for_file_at
from ..helpers.path_repr import get_short_path_repr
from ..test_case import TestCase
from ..wrappers import WrapperBase

from .load_failure import TestFileLoadFailure


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
    value : `object`
        The variable's value.
    
    Returns
    -------
    is_test : `bool`
    """
    if not is_test_name(name):
        return False
    
    if isinstance(value, WrapperBase):
        return value.has_bound_test()
    
    if isinstance(value, FunctionType):
        return True
    
    return False


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
    _results : `None`, `list` of ``Result``
        Results of already ran tests.
    _sub_files : `None`, `list` of ``TestFile``
        Sub files if we are a directory.
    _test_cases : `None`, `list` of ``TestCase``
        The collected test_cases from the file if any. These test_cases are on collected after calling ``.get_test_cases`` for
        the first time.
    entry : ``FileSystemEntry``
        The test file's respective file's or directory's entry in the file system.
    path_parts : `tuple<str>`
        Path parts from the base path to import the file from.
    
    Utility Methods
    ---------------
    - Checks & State
    
        - ``.is_loaded_with_success``
        - ``.is_loaded_with_failure``
        - ``.get_load_failure``
        - ``.is_directory``
        - ``.is_loaded``
        - ``.has_failed_test``
    
    - Iterators
    
        - ``.iter_results``
        - ``.iter_passed_results``
        - ``.iter_skipped_results``
        - ``.iter_failed_results``
        - ``.iter_sub_files``
    
    - Counters
    
        - ``.get_test_case_count``
        - ``.get_ran_test_count``
        - ``.get_passed_test_count``
        - ``.get_skipped_test_count``
        - ``.get_failed_test_count``
        - ``.get_test_file_count``
    
    - Internal
        
        - ``.get_module``
        - ``.try_load_test_cases``
        - ``.get_test_cases``
        - ``.iter_test_cases``
        - ``.iter_invoke_test_cases``
        - ``.feed_sub_file``
        - ``.iter_test_files``
    """
    __slots__ = (
        '__weakref__', '_load_failure', '_module', '_results', '_sub_files', '_test_cases', 'entry', 'path_parts'
    )
    
    def __new__(cls, entry):
        """
        Creates an new test file.
        
        Parameters
        ----------
        entry : ``FileSystemEntry``
            The test file's respective file's or directory's entry in the file system.
        """
        entry.mark_as_used()
        name = entry.get_name()
        
        path_parts = [*(sub_entry.get_name() for sub_entry in entry.iter_parents())]
        if not name == '__init__.py':
            path_parts.append(name)
            
            if path_parts:
                last_path_part = path_parts[-1]
                if last_path_part.endswith('.py'):
                    path_parts[-1] = last_path_part[:-len('.py')]
        
        self = object.__new__(cls)
        self._load_failure = None
        self._module = None
        self._results = None
        self._sub_files = None
        self._test_cases = None
        self.entry = entry
        self.path_parts = path_parts
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
        
        repr_parts.append(' path = ')
        repr_parts.append(get_short_path_repr(self.path))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @property
    def import_route(self):
        """
        Returns the import route from the base path to import the file from.
        
        Returns
        -------
        import_route : `str`
        """
        return '.'.join(self.path_parts)
    
    
    @property
    def path(self):
        """
        Returns the full path of the represented file.
        
        Returns
        -------
        path : `str`
        """
        return self.entry.get_path()
    
    
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
        
        module = modules[import_route]
        self._module = module
        return True
    
    
    def try_load_test_cases(self):
        """
        Loads the file's test_cases. Does method if the test file is a directory.
        
        If loading fails, returns an object representing its failure.
        
        Returns
        -------
        loaded : `bool`
            Whether the tests loaded.
        """
        if self.is_directory():
            return False
        
        module = self.get_module()
        if module is None:
            return False
        
        test_cases = []
        
        for name, value in module.__dict__.items():
            if is_test(name, value):
                test_cases.append(TestCase(self, name, value))
        
        test_cases.sort(key = _test_case_sort_key)
        
        self._test_cases = test_cases
        return True
    
    
    def is_loaded(self):
        """
        Returns whether the test file was loaded.
        
        Returns
        -------
        is_loaded : `bool`
        """
        return self._module is not None
    
    
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
        return [*self.iter_test_cases()]
    
    
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
        
        for sub_file in self.iter_sub_files():
            yield from sub_file.iter_test_cases()
    
    
    def iter_invoke_test_cases(self, environment_manager):
        """
        Iterates over the test cases of the file and invokes them. Yields the test cases' results. If the file is a
        directory will do nothing.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        environment_manager : ``EnvironmentManager``
            Testing environment manager.
        
        Yields
        ------
        result : ``Result``
        """
        if self.is_directory():
            return
        
        results = self._results
        if (results is not None):
            return (yield from results)
        
        environment_manager = apply_environments_for_file_at(environment_manager, self.path)
        for test_case in self.iter_test_cases():
            for result in test_case.iter_invoke(environment_manager):
                if (results is None):
                    results = []
                    self._results = results
                
                results.append(result)
                
                yield result
    
    
    def iter_results(self):
        """
        Iterates over the results of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result : ``Result``
        """
        results = self._results
        if (results is not None):
            yield from results
        
        for sub_file in self.iter_sub_files():
            yield from sub_file.iter_results()
    
    
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
        
        for sub_file in self.iter_sub_files():
            test_count += sub_file.get_test_case_count()
        
        return test_count
    
    
    def get_ran_test_count(self):
        """
        Returns how much tests already ran of the file.
        
        Returns
        -------
        ran_test_count : `int`
        """
        results = self._results
        if (results is None):
            ran_test_count = 0
        else:
            ran_test_count = len(results)
        
        for sub_file in self.iter_sub_files():
            ran_test_count += sub_file.get_ran_test_count()
        
        return ran_test_count
    
    
    def iter_passed_results(self):
        """
        Iterates over the passed results of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result : ``Result``
        """
        for result in self.iter_results():
            if result.is_passed():
                yield result
    
    
    def iter_skipped_results(self):
        """
        Iterates over the skipped results of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result : ``Result``
        """
        for result in self.iter_results():
            if result.is_skipped():
                yield result
    
    
    def iter_failed_results(self):
        """
        Iterates over the failed results of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result : ``Result``
        """
        for result in self.iter_results():
            if result.is_failed():
                yield result
    
    
    def iter_informal_results(self):
        """
        Iterates over the informal results of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result : ``Result``
        """
        for result in self.iter_results():
            if result.is_informal():
                yield result
    
    
    def get_passed_test_count(self):
        """
        Returns how much test passed.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(result.is_passed() for result in self.iter_results())
    
    
    def get_skipped_test_count(self):
        """
        Returns how much test was skipped.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(result.is_skipped() for result in self.iter_results())
    
    
    def get_failed_test_count(self):
        """
        Returns how much test failed.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(result.is_failed() for result in self.iter_results())
    
    
    def has_failed_test(self):
        """
        Returns whether there were any failed tests.
        
        Returns
        -------
        has_failed_tests : `bool`
        """
        return any(result.is_failed() for result in self.iter_results())
    
    
    def feed_sub_file(self, sub_file):
        """
        Adds a sub-file if the file is a directory.
        
        Parameters
        ----------
        sub_file : ``TestFile``
            The sub file to add.
        
        Returns
        -------
        added : `bool`
            Whether the file was added.
        """
        if not self.is_directory():
            return False
        
        sub_files = self._sub_files
        if (sub_files is None):
            sub_files = []
            self._sub_files = sub_files
        
        sub_files.append(sub_file)
        return True
    
    
    def is_directory(self):
        """
        Returns whether the file is a directory.
        
        Returns
        -------
        is_directory : `bool`
        """
        return self.entry.get_name() == '__init__.py'
    
    
    def iter_sub_files(self):
        """
        Iterates over the sub-files registered under this test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        test_file : ``TestFile``
        """
        sub_files = self._sub_files
        if (sub_files is not None):
            yield from sub_files
    
    
    def get_test_file_count(self):
        """
        Returns how much test files the test file contains including itself.
        
        Returns
        -------
        test_file_count : `int`
        """
        test_file_count = 1
        
        for sub_file in self.iter_sub_files():
            test_file_count += sub_file.get_test_file_count()
        
        return test_file_count
    
    
    def iter_test_files(self):
        """
        Iterates over the test files. This includes self and the optionally registered sub-files.
        
        This method is an iterable generator.
        
        Yields
        ------
        test_file : ``TestFile``
        """
        yield self
        
        for sub_file in self.iter_sub_files():
            yield from sub_file.iter_test_files()
