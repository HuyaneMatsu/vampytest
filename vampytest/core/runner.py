__all__ = ('run_tests_in', )

from os.path import isfile as is_file, split as split_paths
from sys import path as system_paths, modules as system_modules

from .. import __package__ as PACKAGE_NAME

from .exceptions import TestLoadingError
from .output_writer import OutputWriter
from .test_file import __file__ as VAMPYTEST_TEST_FILE_PATH
from .test_file_collector import collect_test_files

from scarletio import render_exception_into


def ignore_module_import_frame(file_name, name, line_number, line):
    """
    Ignores the frame, where the test file was imported.
    
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


def try_collect_tests(test_file, output_writer):
    """
    Collects tests from the test files.
    
    Parameters
    ----------
    test_file : ``TestFile``
        The test file to collect tests from.
    output_writer : ``OutputWriter``
        Output writer to write errors to.
    
    Returns
    -------
    collection_successful : `bool`
        Whether no exception occurred.
    """
    try:
        test_file.get_tests()
    except TestLoadingError as err:
        exception_parts = [
            'Exception occurred meanwhile loading:\n',
            test_file.path,
            '\n',
        ]
        
        render_exception_into(err.source_exception, exception_parts, filter=ignore_module_import_frame)
        
        output_writer.write_break_line()
        output_writer.write(''.join(exception_parts))
        output_writer.write_break_line()
        
        collection_successful = False
    
    else:
        collection_successful = True
    
    return collection_successful


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


def test_result_group_sort_key(test_result_group):
    """
    Used to sort result test groups by their name.
    
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
    if is_file(base_path):
        base_path, file_name = split_paths(base_path)
        path_parts.insert(0, file_name)
    
    if base_path in system_paths:
        base_path_in_system_paths = True
    else:
        system_paths.append(base_path)
        base_path_in_system_paths = False
    
    setup_test_library_import()
    
    output_writer = OutputWriter()
    
    try:
        test_files = collect_test_files(base_path, path_parts)
        
        output_writer.write(f'Collected {len(test_files)} test file(s).')
        
        test_files = [test_file for test_file in test_files if try_collect_tests(test_file, output_writer)]
        
        total_test_count = 0
        for test_file in test_files:
            total_test_count += len(test_file.get_tests())
        
        output_writer.write(f'Running {total_test_count} tests of {len(test_files)} files')
        output_writer.write_break_line()
        
        test_result_groups = []
        
        for test_file in test_files:
            for test in test_file.get_tests():
                test_result_group = test.invoke()
                test_result_groups.append(test_result_group)
        
        test_result_groups.sort(key=test_result_group_sort_key)
        
        failed_tests = []
        passed_test_count = 0
        skipped_test_count = 0
        
        for test_result_group in test_result_groups:
            if test_result_group.is_skipped():
                skipped_test_count += 1
                keyword = 'S'
            
            elif test_result_group.is_passed():
                passed_test_count += 1
                keyword = 'P'
            
            elif test_result_group.is_failed():
                failed_tests.append(test_result_group)
                keyword = 'F'
            
            else:
                keyword = '?'
            
            case = test_result_group.case
            
            output_writer.write(f'{keyword} {case.import_route}.{case.name}')
        
        output_writer.write_break_line()
        
        for test_result_group in failed_tests:
            for failure_message in test_result_group.iter_failure_messages():
                output_writer.write(failure_message)
                output_writer.write_break_line()
        
        output_writer.write(f'{len(failed_tests)} failed | {skipped_test_count} skipped | {passed_test_count} passed')
        
        # Close output with an empty line.
        output_writer.write('\n')
    
    finally:
        if base_path_in_system_paths:
            try:
                system_paths.remove(base_path)
            except ValueError:
                pass
