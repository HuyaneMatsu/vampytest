__all__ = ('iter_collect_test_files_in',)

from .test_file import TestFile


def iter_collect_test_files_in(entry):
    """
    Iterates over the given file system entry and yields back the collected test files.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    entry : ``FileSystemEntry``
        The entry to iterate over.
    
    Yields
    ------
    test_file : ``TestFile``
    """
    if entry.is_directory():
        yield from iter_collect_test_files_in_directory(entry, is_test_directory_name(entry.get_name()))
        entry.purge()
        return
    
    if is_test_file_name(entry.get_name()):
        yield TestFile(entry)
        return
    
    # no more cases
    return


def iter_collect_test_files_in_directory(entry, within_test_directory):
    """
    Iterates over a directory discovering test files.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    entry : ``FileSystemEntry``
        The entry to iterate over.
    within_test_directory : `bool`
        Defines whether we are in a test directory and whether we should collect test files from it.
    
    Yields
    ------
    test_file : ``TestFile``
    """
    # First check directory
    if within_test_directory:
        directory = None
        
        for sub_entry in entry.iter_entries():
            if sub_entry.is_file():
                name = sub_entry.get_name()
                if name == '__init__.py':
                    directory = TestFile(sub_entry)
                    continue
                
                if is_test_file_name(name):
                    test_file = TestFile(sub_entry)
                    
                    if (directory is None):
                        yield test_file
                        continue
                    
                    directory.feed_sub_file(test_file)
                    continue
        
        if (directory is not None):
            yield directory
    
    else:
        for sub_entry in entry.iter_entries():
            if sub_entry.is_directory():
                yield from iter_collect_test_files_in_directory(sub_entry, is_test_directory_name(sub_entry.get_name()))
                sub_entry.purge()


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
    
    if file_name in ('test.py', 'tests.py'):
        return True
    
    if file_name.startswith('test_') and file_name.endswith('.py') and (len(file_name) > (len('test_') + len('.py'))):
        return True
    
    if file_name.endswith('_tests.py') and (len(file_name) > len('_tests.py')):
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
    if directory_name.startswith('_'):
        return False
    
    if directory_name == 'tests':
        return True
    
    if directory_name.startswith('test_') and (len(directory_name) > len('test_')):
        return True
    
    if directory_name.startswith('tests_') and (len(directory_name) > len('tests_')):
        return True
    
    if directory_name.endswith('_tests') and (len(directory_name) > len('_tests')):
        return True
    
    return False
