__all__ = ('RunnerContext',)

from scarletio import RichAttributeErrorBaseType


class RunnerContext(RichAttributeErrorBaseType):
    """
    Represents a test's context. Test contexts are present while running a test.
    
    Attributes
    ----------
    _registered_files : `None`, `list` of ``TestFile``
        The collected test files.
    runner : ``TestRunner``
        The respective test runner running tests.
    
    Utility Methods
    ---------------
    - Count getters
    
        - ``.get_registered_file_count``
        - ``.get_test_case_count``
        - ``.get_ran_test_count``
        - ``.get_passed_test_count``
        - ``.get_skipped_test_count``
        - ``.get_failed_test_count``
        - ``.get_load_failed_file_count``
        - ``.get_load_succeeded_file_count``
    
    - Iterators
    
        - ``.iter_registered_files``
        - ``.iter_result_groups``
        - ``.iter_passed_result_groups``
        - ``.iter_skipped_result_groups``
        - ``.iter_failed_result_groups``
        - ``.iter_load_failed_files``
        - ``.iter_load_succeeded_files``
        - ``.iter_file_load_failures``
    
    - Getters
    
        - ``.get_registered_files``
        - ``.get_failed_to_load``
        - ``.get_file_load_failures``
        - ``.get_skipped_result_groups``
        - ``.get_failed_result_groups``
        - ``.get_load_failed_file_count``
    
    - Internal
    
        - ``.register_file``
    """
    __slots__ = ('_registered_files', 'runner',)
    
    def __new__(cls, runner):
        """
        
        Parameters
        ----------
        runner : ``TestRunner``
            The respective test runner running tests.
        """
        self = object.__new__(cls)
        self._registered_files = None
        self.runner = runner
        return self
    
    
    def get_registered_file_count(self):
        """
        Returns how much much registered files were collected.
        """
        registered_file_count = 0
        
        for registered_file in self.iter_registered_files():
            registered_file_count += registered_file.get_test_file_count()
        
        return registered_file_count
    
    
    def iter_registered_files_shallow(self):
        """
        Shallow iterates over the registered files.
        
        This method is an iterable generator.
        
        Yields
        ------
        registered_file : ``TestFile``
        """
        registered_files = self._registered_files
        if (registered_files is not None):
            yield from registered_files
    
    
    def iter_registered_files(self):
        """
        Iterates over the registered files.
        
        This method is an iterable generator.
        
        Yields
        ------
        registered_file : ``TestFile``
        """
        registered_files = self._registered_files
        if (registered_files is not None):
            for registered_file in registered_files:
                yield from registered_file.iter_test_files()
    
    
    def get_registered_files(self):
        """
        Returns a copy of the registered files.
        
        Returns
        -------
        registered_files : `list` of ``TestFile``
        """
        return [*self.iter_registered_files()]
    
    
    def register_file(self, registered_file):
        """
        Adds a new registered file.
        
        Parameters
        ----------
        registered_file : ``TestFile``
        """
        registered_files = self._registered_files
        if registered_files is None:
            registered_files = []
            self._registered_files = registered_files
        
        registered_files.append(registered_file)
    
    
    def get_test_case_count(self):
        """
        Returns how much test cases are in the test files collected.
        
        Returns
        -------
        test_case_count : `int`
        """
        return sum(test_file.get_test_case_count() for test_file in self.iter_registered_files())
    
    
    def get_ran_test_count(self):
        """
        Returns how much tests already ran.
        
        Returns
        -------
        ran_test_count : `int`
        """
        return sum(test_file.get_ran_test_count() for test_file in self.iter_registered_files())
    
    
    def iter_result_groups(self):
        """
        Iterates over the result groups.
        
        This method is an iterable generator.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        for test_file in self.iter_registered_files():
            yield from test_file.iter_result_groups()
    
    
    def iter_passed_result_groups(self):
        """
        Iterates over the passed result groups of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        for test_file in self.iter_registered_files():
            yield from test_file.iter_passed_result_groups()
    
    
    def iter_skipped_result_groups(self):
        """
        Iterates over the skipped result groups of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        for test_file in self.iter_registered_files():
            yield from test_file.iter_skipped_result_groups()
    
    
    def iter_failed_result_groups(self):
        """
        Iterates over the failed result groups of the test file.
        
        This method is an iterable generator.
        
        Yields
        ------
        result_group : ``ResultGroup``
        """
        for test_file in self.iter_registered_files():
            yield from test_file.iter_failed_result_groups()
    
    
    def get_passed_test_count(self):
        """
        Returns how much test passed.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(test_file.get_passed_test_count() for test_file in self.iter_registered_files())
    
    
    def get_skipped_test_count(self):
        """
        Returns how much test was skipped.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(test_file.get_skipped_test_count() for test_file in self.iter_registered_files())
    
    
    def get_failed_test_count(self):
        """
        Returns how much test failed.
        
        Returns
        -------
        passed_test_count : `int`
        """
        return sum(test_file.get_failed_test_count() for test_file in self.iter_registered_files())
    
    
    def get_passed_result_groups(self):
        """
        Iterates over the passed result groups of the test file.
        
        Returns
        -------
        result_groups : `list` of ``ResultGroup``
        """
        return [*self.iter_passed_result_groups()]
    
    
    def get_skipped_result_groups(self):
        """
        Iterates over the skipped result groups of the test file.
        
        Returns
        -------
        result_groups : `list` of ``ResultGroup``
        """
        return [*self.iter_skipped_result_groups()]
    
    
    def get_failed_result_groups(self):
        """
        Iterates over the failed result groups of the test file.
        
        Returns
        -------
        result_groups : `list` of ``ResultGroup``
        """
        return [*self.iter_failed_result_groups()]
    
    
    def get_load_failed_file_count(self):
        """
        Returns how much files failed to load.
        
        Returns
        -------
        load_failed_file_count : `bool`
        """
        return sum(test_file.is_loaded_with_failure() for test_file in self.iter_registered_files())
    
    
    def get_load_succeeded_file_count(self):
        """
        Returns how much files failed to load.
        
        Returns
        -------
        load_succeeded_file_count : `bool`
        """
        return sum(test_file.is_loaded_with_success() for test_file in self.iter_registered_files())
    
    
    def get_not_loaded_file_count(self):
        """
        Returns how much file was not loaded.
        
        Returns
        -------
        not_loaded_file_count : `bool`
        """
        return sum((not test_file.is_loaded()) for test_file in self.iter_registered_files())
    
    
    def iter_load_failed_files(self):
        """
        Iterates over the files which failed to load.
        
        This method is an iterable generator.
        
        Yields
        -------
        test_file : ``TestFile``
        """
        for test_file in self.iter_registered_files():
            if test_file.is_loaded_with_failure():
                yield test_file
    
    
    def iter_load_succeeded_files(self):
        """
        Iterates over the files which succeeded to load.
        
        This method is an iterable generator.
        
        Yields
        -------
        test_file : ``TestFile``
        """
        for test_file in self.iter_registered_files():
            if test_file.is_loaded_with_success():
                yield test_file
    
    
    def iter_file_load_failures(self):
        """
        Iterates over the file load failures.
        
        This method is an iterable generator.
        
        Yields
        -------
        load_failure : ``TestFileLoadFailure``
        """
        for test_file in self.iter_registered_files():
            load_failure = test_file.get_load_failure()
            if (load_failure is not None):
                yield load_failure
    
    
    def get_file_load_failures(self):
        """
        Returns the file load failures.
        
        Returns
        -------
        load_failures : `list` of ``TestFileLoadFailure``
        """
        return [*self.iter_file_load_failures()]
