__all__ = ('collect_test_files', )

from os import listdir as list_directory
from os.path import isabs as is_absolute_path_name, isdir as is_directory, isfile as is_file, join as join_paths

from .test_file import TestFile

# TODO

def collect_test_files(path):
    return list(iter_collect_test_files(path))


def iter_collect_test_files(path):
    """
    Iterates over the given directory or file path.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    path : `str`
        Source path of file or directory.
    
    Yields
    ------
    test_file : ``TestFile``
    """
    # pretty weird case
    if is_file(path):
        yield TestFile(path)
    
    if is_directory(path):
        yield from iter_tests_from_directory(path, False)


def is_test_file_name(file_name):
    """
    Returns whether the given file name is the name of a test file.
    
    Parameters
    ----------
    file_name : `str`
        A file's name.
    
    Returns
    -------
    is_test_file_name : `bool`
    """
    if file_name == 'test.py':
        return True
    
    if file_name.startswith('test_') and file_name.endswith('.py'):
        return True
    
    if file_name.endswith('_tests.py'):
        return True
    
    return False


def is_test_directory_name(directory_name):
    """
    Returns whether the given directory name is a name of a test directory.
    
    Parameters
    ----------
    directory_name : `str`
        A directory's name.
    
    Returns
    -------
    is_test_directory_name : `bool`
    """
    if directory_name == 'tests':
        return True
    
    if directory_name.startswith('test_'):
        return True
    
    if directory_name.endswith('_tests'):
        return True
    
    return False


def iter_tests_from_directory(directory_path, within_test_directory):
    """
    Iterates over a directory discovering test files.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    within_test_directory : `bool`
        Defines whether
    
    Yields
    ------
    test_file : ``TestFile``
    """
    for file_name in list_directory(directory_path):
        file_path = join_paths(directory_path, file_name)
        
        if is_file(file_path):
            if within_test_directory and is_test_file_name(file_name):
                yield TestFile(file_path)
        
        if is_directory(file_path):
            yield from iter_tests_from_directory(file_path, is_test_directory_name(file_name))
