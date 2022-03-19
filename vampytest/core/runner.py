__all__ = ('run_tests_in', )

from os.path import isfile as is_file, split as split_paths
from sys import path as system_paths, stdout

from .exceptions import TestLoadingError
from .test_file import __file__ as VAMPYTEST_TEST_FILE_PATH
from .test_file_collector import collect_test_files

from scarletio import render_exception_into


def ignore_module_import_frame(file_name, name, line_number, line):
    """
    Parameters
    ----------
    file_name : `str`
        The frame's respective file's name.
    name : `str`
        The frame's respective function's name.
    line_number : `int`
        The line's index where the exception occurred.
    line : `str`
        The frame's respective stripped line.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    return (file_name != VAMPYTEST_TEST_FILE_PATH) or (name != '_get_module') or (line != '__import__(import_route)')


def try_collect_tests(test_file):
    """
    Collects tests from the test files.
    
    Parameters
    ----------
    test_file : ``TestFile``
        The test file to collect tests from.
    
    Returns
    -------
    collection_successful : `bool`
        Whether no exception occurred.
    """
    try:
        test_file.get_tests()
    except TestLoadingError as err:
        exception_parts = [
            '='*40,
            '\nException occurred meanwhile loading:\n',
            test_file.path,
            '\n',
        ]
        
        render_exception_into(err.source_exception, exception_parts, filter=ignore_module_import_frame)
        
        exception_parts.append('='*40)
        exception_parts.append('\n')
        
        stdout.write(''.join(exception_parts))
        collection_successful = False
    
    else:
        collection_successful = True
    
    return collection_successful


def run_tests_in(base_path, path_parts):
    if is_file(base_path):
        base_path, file_name = split_paths(base_path)
        path_parts.insert(0, file_name)
    
    if base_path in system_paths:
        base_path_in_system_paths = True
    else:
        system_paths.append(base_path)
        base_path_in_system_paths = False
    
    try:
        test_files = collect_test_files(base_path, path_parts)
        
        stdout.write(f'Collected {len(test_files)} test file(s).\n')
        
        test_files = [test_file for test_file in test_files if try_collect_tests(test_file)]
        
        total_test_count = 0
        for test_file in test_files:
            total_test_count += len(test_file.get_tests())
        
        stdout.write(f'Running {total_test_count} tests of {len(test_files)} files\n')
        for test_file in test_files:
            for test in test_file.get_tests():
                test.invoke()
    
    
    finally:
        if base_path_in_system_paths:
            try:
                system_paths.remove(base_path)
            except ValueError:
                pass
