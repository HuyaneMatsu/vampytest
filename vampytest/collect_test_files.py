__all__ = ('collect_test_files',)

from os import listdir as list_directory
from os.path import isabs as is_absolute_path_name, isdir as is_directory, isfile as is_file, join as join_paths

from .test_file import TestFile

# TODO

def collect_test_files(path):
    return list(iter_collect_test_files(path))


def iter_collect_test_files(path):
    # pretty weird case
    if is_file(path):
        yield TestFile(path)
    
    if is_directory(path):
        yield from iter_tests_from_directory(path)

def iter_tests_from_directory(directory_path):
    for file_name in list_directory(directory_path):
        file_path = join_paths(directory_path, file_name)
        
        if is_file(file_path):
            if (
                file_name == 'test.py' or
                (
                    file_name.startswith('.py') and
                    file_name.endswith('.py')
                )
            ):
                yield TestFile(file_path)
