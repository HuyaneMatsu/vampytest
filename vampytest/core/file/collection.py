__all__ = ('iter_collect_test_files',)

from os import listdir as list_directory
from os.path import isdir as is_directory, isfile as is_file, join as join_paths

from .test_file import TestFile


def iter_collect_test_files(base_path, path_parts):
    """
    Iterates over the given directory or file path.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    base_path : `str`
        Source path of file or directory.
    path_parts : `list` of `str`
        A list of path parts within the base directory to collect from.
    
    Yields
    ------
    test_file : ``TestFile``
    """
    # pretty weird case
    path_parts = path_parts.copy()
    path = join_paths(base_path, *path_parts)
    if is_file(path):
        yield TestFile(path, path_parts, False)
        return
    
    if is_directory(path):
        yield from iter_tests_from_directory(path, path_parts, False)
        return
    
    # no more cases
    return


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
    if file_name.startswith('_'):
        return False
    
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
    
    if directory_name.startswith(('test_', 'tests_')):
        return True
    
    if directory_name.endswith('_tests'):
        return True
    
    return False


def iter_tests_from_directory(directory_path, path_parts, within_test_directory):
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
    file_names = list_directory(directory_path)
    file_names.sort()
    
    # First check directory
    if within_test_directory:
        directory = None
        for file_name in file_names:
            file_path = join_paths(directory_path, file_name)
            path_parts.append(file_name)
            
            if is_file(file_path):
                if file_name == '__init__.py':
                    directory = TestFile(file_path, path_parts, True)
                
                elif is_test_file_name(file_name):
                    test_file = TestFile(file_path, path_parts, False)
                    
                    if (directory is None):
                        yield test_file
                    
                    else:
                        directory.feed_sub_file(test_file)
            
            del path_parts[-1]
        
        if (directory is not None):
            yield directory
    
    else:
        for file_name in file_names:
            file_path = join_paths(directory_path, file_name)
            path_parts.append(file_name)
            
            if is_directory(file_path):
                yield from iter_tests_from_directory(file_path, path_parts, is_test_directory_name(file_name))
            
            del path_parts[-1]
