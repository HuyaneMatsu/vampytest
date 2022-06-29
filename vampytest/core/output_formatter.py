__all__ = ('OutputFormatter',)

from .output_writer import OutputWriter

from scarletio import RichAttributeErrorBaseType


class OutputFormatter(RichAttributeErrorBaseType):
    """
    Output formatter for test runner.
    
    Attributes
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    test_files : `None`, `list` of `TestFile`
        The collected test files.
    loaded_test_files : `None`, `list` of ``TestFile``
        The test files which have been successfully loaded.
    load_failures : `None`, `list` of ``TestFileLoadFailure``
        Load failures.
    result_groups : `None`, `list` of ``ResultGroup``
    """
    __slots__ = ('output_writer', 'test_files', 'loaded_test_files', 'load_failures', 'result_groups')
    
    def __new__(cls, output_writer=None):
        """
        Parameters
        ----------
        output_writer : `None`, ``OutputWriter` = `None`, Optional
            The output writer to write the output with.
        """
        if (output_writer is None):
            output_writer = OutputWriter()
        
        self = object.__new__(cls)
        self.output_writer = output_writer
        self.test_files = None
        self.loaded_test_files = None
        self.load_failures = None
        self.result_groups = None
        return self
    
    
    def __repr__(self):
        """Returns the output writer's representation."""
        return f'<{self.__class__.__name__} output_writer={self.output_writer!r}>'
    
    
    def files_collected(self, test_files):
        """
        Called when collecting test files is finished.
        
        Parameters
        ----------
        test_files : `list` of ``TestFile``
            The collected test files.
        """
        self.test_files = test_files
        self.render_files_collected()
    
    
    def files_loaded(self, loaded_test_files, load_failures):
        """
        Called when loading the test files is finished.
        
        Parameters
        ----------
        loaded_test_files : `list` of ``TestFile``
            The test files which have been successfully loaded.
        load_failures : `list` of ``TestFileLoadFailure``
            Load failures.
        """
        self.loaded_test_files = loaded_test_files
        self.load_failures = load_failures
        self.render_files_loaded()
    
    
    def tests_ran(self, result_groups):
        """
        Called when the tests ran.
        """    
        self.result_groups = result_groups
        self.render_tests_done()
    
    
    def render_files_collected(self):
        """
        Called to render the collected test files to render the testing state to the output writer.
        """
        test_files = self.test_files
        if (test_files is None):
            test_file_count = 0
        else:
            test_file_count = len(test_files)
        
        output_writer = self.output_writer
        output_writer.write_line(f'Collected {test_file_count} test file(s).')
        output_writer.write_break_line()
    
    
    def render_files_loaded(self):
        """
        Called when the test files are loaded to render the testing state to the output writer.
        """
        load_failures = self.load_failures
        loaded_test_files = self.loaded_test_files
        
        output_writer = self.output_writer
        if (load_failures is not None) and load_failures:
            output_writer.write_line(f'{len(load_failures)} files failed to load')
            output_writer.write_break_line()
            
            for load_failure in load_failures:
                output_writer.write_line(load_failure.get_full_message())
                output_writer.write_break_line()
        
        
        if (loaded_test_files is None):
            loaded_test_file_count = 0
            total_test_count = 0
        
        else:
            loaded_test_file_count = len(loaded_test_files)
            
            total_test_count = 0
            for test_file in loaded_test_files:
                total_test_count += len(test_file.get_tests())
        
        output_writer.write(f'Running {total_test_count} tests of {loaded_test_file_count} files')
        if (load_failures is not None) and load_failures:
            output_writer.write(f' | {len(load_failures)} files failed to load')
        output_writer.end_line()
        
        output_writer.write_break_line()
    
    
    def render_tests_done(self):
        """
        Called when all tests finished running.
        """
        output_writer = self.output_writer
        
        failed_tests = []
        passed_test_count = 0
        skipped_test_count = 0
        
        result_groups = self.result_groups
        
        if (result_groups is not None):
            for result_group in result_groups:
                if result_group.is_skipped():
                    skipped_test_count += 1
                    keyword = 'S'
                
                elif result_group.is_passed():
                    passed_test_count += 1
                    keyword = 'P'
                
                elif result_group.is_failed():
                    failed_tests.append(result_group)
                    keyword = 'F'
                
                else:
                    keyword = '?'
                
                case = result_group.case
                
                output_writer.write_line(f'{keyword} {case.import_route}.{case.name}')
        
        output_writer.write_break_line()
        
        for result_group in failed_tests:
            for failure_message in result_group.iter_failure_messages():
                output_writer.write_line(failure_message)
                output_writer.write_break_line()
        
        output_writer.write(f'{len(failed_tests)} failed | {skipped_test_count} skipped | {passed_test_count} passed')
        load_failures = self.load_failures
        if (load_failures is not None) and load_failures:
            output_writer.write(f' | {len(load_failures)} files failed to load')
        output_writer.end_line()
