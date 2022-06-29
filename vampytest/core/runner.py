__all__ = ('TestRunner', 'run_tests_in')

from functools import partial as partial_func
from os.path import isfile as is_file, split as split_paths
from sys import path as system_paths, modules as system_modules

from .. import __package__ as PACKAGE_NAME

from .test_file import collect_test_files
from .output_formatter import OutputFormatter


from scarletio import RichAttributeErrorBaseType


def setup_test_library_import():
    """
    Setups test directory import if not on path instead running it relatively.
    
    Returns
    -------
    added_system_path : `None`, `str`
        Returns the added system path if any.
    """
    split = PACKAGE_NAME.split('.')
    if len(split) <= 1:
        return None
    
    module = __import__(PACKAGE_NAME)
    for directory_name in split[1:]:
        module = module.__dict__[directory_name]
    
    system_modules[split[-1]] = module


def _remove_from_system_path_callback(path, runner):
    """
    Removes the given path from `sys.path`.
    
    Parameters
    ----------
    path : `str`
        The path to remove.
    runner : ``TestRunner``
        The respective test runner.
    """
    try:
        system_paths.remove(path)
    except ValueError:
        pass


def try_load_test_files(test_files):
    """
    Tries to load the given test files.
    
    Parameters
    ----------
    test_files : `list` of ``TestFile``
        The test files to load.
    
    Returns
    -------
    loaded_test_files : `list` of ``TestFile``
        The test files which have been successfully loaded.
    load_failures : `list` of ``TestFileLoadFailure``
        Load failures.
    """
    loaded_test_files = []
    load_failures = []
    
    for test_file in test_files:
        load_failure = test_file.try_load_tests()
        if (load_failure is None):
            loaded_test_files.append(test_file)
        
        else:
            load_failures.append(load_failure)
    
    return loaded_test_files, load_failures


def _test_result_group_sort_key(test_result_group):
    """
    Used to sort test result groups by their name.
    
    Parameters
    ----------
    test_result_group : ``ResultGroup``
        Test result group to get sort key of.
    
    Returns
    -------
    sort_key : `tuple` (`str`, `str`)
    """
    case = test_result_group.case
    key = (case.import_route, case.name)
    return key


def run_tests(test_files):
    """
    Runs the tests of the given test files.
    
    Parameters
    ----------
    test_files : `list` of ``TestFile``
        The test files to run.
    
    Returns
    -------
    result_groups : ``ResultGroup``
    """
    test_result_groups = []
    
    for test_file in test_files:
        for test_case in test_file.get_tests():
            test_result_group = test_case.invoke()
            test_result_groups.append(test_result_group)
        
    test_result_groups.sort(key=_test_result_group_sort_key)
    
    return test_result_groups


class TestRunner(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    _base_path : `str`
        The path to run tests from.
    _path_parts : `list` of `str`   
        Added path parts to specify from which which directory we want to collect the tests from.
    _teardown_callbacks : `None`, `list` of `callable`
        Functions to call when the tests are finished.
    output_formatter : ``OutputFormatter``
        Output writer used to render the exception messages with.
    """
    __slots__ = ('_base_path', '_path_parts', '_teardown_callbacks', 'output_formatter')
    
    def __new__(cls, base_path, path_parts=None, *, output_formatter=None):
        """
        Parameters
        ----------
        base_path : `str`
            The path to run tests from.
        path_parts : `None`, `list` of `str` = `None`, Optional
            Added path parts to specify from which which directory we want to collect the tests from.
        output_formatter : `None`, ``OutputFormatter`` = `None`, Optional (Keyword only)
            The output writer to use to render the exception messages with.
        """
        if path_parts is None:
            path_parts = []
        else:
            path_parts = path_parts.copy()
        
        if output_formatter is None:
            output_formatter = OutputFormatter()
        
        self = object.__new__(cls)
        self._base_path = base_path
        self._path_parts = path_parts
        self._teardown_callbacks = None
        self.output_formatter = output_formatter
        return self
    
    
    def setup(self):
        """
        Setups the test dependencies.
        """
        base_path = self._base_path
        path_parts = self._path_parts
        
        if is_file(base_path):
            base_path, file_name = split_paths(base_path)
            path_parts.insert(0, file_name)
        
        if base_path in system_paths:
            base_path_in_system_paths = True
        else:
            system_paths.append(base_path)
            base_path_in_system_paths = False
        
        self._base_path = base_path
        self._path_parts = path_parts
        
        if base_path_in_system_paths:
            self.add_teardown_callback(partial_func(_remove_from_system_path_callback, base_path))
        
        setup_test_library_import()
    
    
    def add_teardown_callback(self, callback):
        """
        Adds a callback to run when the tests are finished.
        
        Parameters
        ----------
        callback : `callable`
            The callback to add.
        """
        teardown_callbacks = self._teardown_callbacks
        if (teardown_callbacks is None):
            teardown_callbacks = []
            self._teardown_callbacks = teardown_callbacks
        
        teardown_callbacks.append(callback)
    
    
    def exhaust_teardown_callbacks(self):
        """
        Runs the teardown callbacks.
        """
        teardown_callbacks = self._teardown_callbacks
        self._teardown_callbacks = None
        
        if (teardown_callbacks is not None):
            while teardown_callbacks:
                teardown_callbacks.pop()(self)
    
    
    def teardown(self):
        """
        Clears up after the tests ran.
        """
        self.exhaust_teardown_callbacks()
        
    
    def run(self):
        """
        Runs the tests of the test runner.
        """
        try: 
            self.setup()
            output_formatter = self.output_formatter
            
            collected_test_files = collect_test_files(self._base_path, self._path_parts)
            output_formatter.files_collected(collected_test_files)
            
            loaded_test_files, load_failures = try_load_test_files(collected_test_files)
            output_formatter.files_loaded(loaded_test_files, load_failures)
            
            result_groups = run_tests(loaded_test_files)
            output_formatter.tests_ran(result_groups)
        
        finally:
            self.teardown()


def run_tests_in(base_path, path_parts):
    """
    Runs tests from the given `base_path` and collects them the added `path_parts`.
    
    Parameters
    ----------
    base_path : `str`
        The path to run tests from.
    path_parts : `list` of `str`
        Added path parts to specify from which which directory we want to collect the tests from.
    """
    TestRunner(base_path, path_parts).run()
