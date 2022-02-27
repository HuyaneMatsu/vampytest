__all__ = ('run_tests_in', )

from os.path import isfile as is_file, split as split_paths
from sys import path as system_paths, stdout

from .test_file_collector import collect_test_files


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
        
        stdout.write(f'Collected {len(test_files)} test files\n')
        
        for test_file in test_files:
            tests = test_file.get_tests()
    
    finally:
        if base_path_in_system_paths:
            try:
                system_paths.remove(base_path)
            except ValueError:
                pass
