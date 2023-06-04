__all__ = ('RunState',)

from scarletio import RichAttributeErrorBaseType


class RunState(RichAttributeErrorBaseType):
    """
    Represents a test runner's run state.
    
    Attributes
    ----------
    _load_failures : `None`, `list` of ``TestFileLoadFailure``
        Load failures.
    _loaded_test_files : `None`, `list` of ``TestFile``
        The test files which have been successfully loaded.
    _results : `None`, `list` of ``Result``
        The ran tests' results.
    _test_files : `None`, `list` of ``TestFile``
        The collected test files.
    """
    __slots__ = ('_load_failures', '_loaded_test_files', '_results', '_test_files',)
    
    def __new__(cls):
        """
        Creates a new run state.
        """
        self = object.__new__(cls)
        self._load_failures = None
        self._loaded_test_files = None
        self._results = None
        self._test_files = None
        return self
    
    # generic interaction methods
    
    def get_load_failure_count(self):
        """
        Returns how much much tests files were collected.
        """
        load_failures = self._load_failures
        if (load_failures is None):
            load_failure_count = 0
        else:
            load_failure_count = len(load_failures)
        
        return load_failure_count
    
    
    def iter_load_failures(self):
        """
        Iterates over the load failures.
        
        This method is an iterable generator.
        
        Yields
        ------
        load_failure : ``TestFileLoadFailure``
        """
        load_failures = self._load_failures
        if (load_failures is not None):
            yield from load_failures
    
    
    def get_load_failures(self):
        """
        Returns a copy of the load failures.
        
        Returns
        -------
        load_failures : `list` of ``TestFileLoadFailure``
        """
        load_failures = self._load_failures
        if load_failures is None:
            load_failures = []
        else:
            load_failures = load_failures.copy()
        
        return load_failures
    
    
    def add_load_failure(self, load_failure):
        """
        Adds a new load failure.
        
        Parameters
        ----------
        load_failure : ``TestFileLoadFailure``
        """
        load_failures = self._load_failures
        if load_failures is None:
            load_failures = []
            self._load_failures = load_failures
        
        load_failures.append(load_failure)
    
    

    def get_loaded_test_file_count(self):
        """
        Returns how much much loaded tests files were collected.
        """
        loaded_test_files = self._loaded_test_files
        if (loaded_test_files is None):
            loaded_test_file_count = 0
        else:
            loaded_test_file_count = len(loaded_test_files)
        
        return loaded_test_file_count
    
    
    def iter_loaded_test_files(self):
        """
        Iterates over the loaded  test files.
        
        This method is an iterable generator.
        
        Yields
        ------
        loaded_test_files : ``TestFile``
        """
        loaded_test_files = self._loaded_test_files
        if (loaded_test_files is not None):
            yield from loaded_test_files
    
    
    def get_loaded_test_files(self):
        """
        Returns a copy of the loaded test files.
        
        Returns
        -------
        loaded_test_files : `list` of ``TestFile``
        """
        loaded_test_files = self._loaded_test_files
        if loaded_test_files is None:
            loaded_test_files = []
        else:
            loaded_test_files = loaded_test_files.copy()
        
        return loaded_test_files
    
    
    def add_loaded_test_files(self, loaded_test_file):
        """
        Adds a new loaded test file.
        
        Parameters
        ----------
        loaded_test_file : ``TestFile``
        """
        loaded_test_files = self._loaded_test_files
        if loaded_test_files is None:
            loaded_test_files = []
            self._loaded_test_files = loaded_test_files
        
        loaded_test_files.append(loaded_test_file)
    

    def get_results_count(self):
        """
        Returns how much much tests files were collected.
        
        Returns
        -------
        results_count : `int`
        """
        results = self._results
        if (results is None):
            results_count = 0
        else:
            results_count = len(results)
        
        return results_count
    
    
    def iter_results(self):
        """
        Iterates over the result.
        
        This method is an iterable generator.
        
        Yields
        ------
        results : ``Result``
        """
        results = self._results
        if (results is not None):
            yield from results
    
    
    def get_results(self):
        """
        Returns a copy of the result.
        
        Returns
        -------
        results : `list` of ``Result``
        """
        results = self._results
        if results is None:
            results = []
        else:
            results = results.copy()
        
        return results
    
    
    def add_results(self, result):
        """
        Adds a new result.
        
        Parameters
        ----------
        result : ``Result``
            The result to add.
        """
        results = self._results
        if results is None:
            results = []
            self._results = results
        
        results.append(result)
    
    
    def get_test_file_count(self):
        """
        Returns how much much tests files were collected.
        
        Returns
        -------
        test_file_count : `int`
        """
        test_files = self._test_files
        if (test_files is None):
            test_file_count = 0
        else:
            test_file_count = len(test_files)
        
        return test_file_count
    
    
    def iter_test_files(self):
        """
        Iterates over the test files.
        
        This method is an iterable generator.
        
        Yields
        ------
        test_file : ``TestFile``
        """
        test_files = self._test_files
        if (test_files is not None):
            yield from test_files
    
    
    def get_test_files(self):
        """
        Returns a copy of the test files.
        
        Returns
        -------
        test_files : `list` of ``TestFile``
        """
        test_files = self._test_files
        if test_files is None:
            test_files = []
        else:
            test_files = test_files.copy()
        
        return test_files
    
    
    def add_test_file(self, test_file):
        """
        Adds a new test file.
        
        Parameters
        ----------
        test_file : ``TestFile``
        """
        test_files = self._test_files
        if test_files is None:
            test_files = []
            self._test_files = test_files
        
        test_files.append(test_file)
    
    # Added features
    
    def __repr__(self):
        """Returns the run state's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' loaded_test_files: ')
        repr_parts.append(repr(self.get_loaded_test_file_count()))
        repr_parts.append(' / ')
        repr_parts.append(repr(self.get_test_file_count()))
        
        repr_parts.append(' tests_ran: ')
        repr_parts.append(repr(self.get_results_count()))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_total_registered_test_count(self):
        """
        Returns how much tests were registered by the loaded test files.
        
        Returns
        -------
        total_registered_test_count : `int`
        """
        total_registered_test_count = 0
        
        for test_file in self.iter_loaded_test_files():
            total_registered_test_count += test_file.get_test_count()
        
        return total_registered_test_count
    
    
    def iter_test_cases(self):
        """
        Iterates over the test cases.
        
        Yields
        ------
        test_case : ``TestCase``
        """
        for test_file in self.iter_test_files():
            yield from test_file.iter_tests()
