from ...core import _, assert_instance, call_from, mock_globals

from ..source_lookup import build_project_sources


def _iter_options():
    yield (
        '/orin',
        None,
        None,
        None,
        {},
        None,
    )
    
    yield (
        '/orin',
        object(),
        object(),
        object(),
        {},
        None,
    )
    
    yield (
        '/orin',
        'vampy',
        None,
        None,
        {
            '/orin/vampy/__init__.py',
        },
        {
            'vampy',
        },
    )
    
    yield (
        '/orin',
        None,
        [
            'vampy.eyes'
        ],
        None,
        {
            '/orin/vampy/__init__.py',
        },
        {
            'vampy',
        },
    )
    
    yield (
        '/orin',
        'eyes',
        [
            'vampy.eyes'
        ],
        None,
        {
            '/orin/eyes/__init__.py',
            '/orin/vampy/__init__.py',
        },
        {
            'vampy',
        },
    )
    
    yield (
        '/orin',
        None,
        None,
        [
            'vampy = vampy.__main__:__main__',
        ],
        {
            '/orin/vampy/__init__.py',
        },
        {
            'vampy',
        },
    )
    
    yield (
        '/orin',
        None,
        [
            'vampy.eyes'
        ],
        [
            'eyes = eyes.__main__:__main__',
        ],
        {
            '/orin/eyes/__init__.py',
            '/orin/vampy/__init__.py',
        },
        {
            'vampy',
        },
    )


@_(call_from(_iter_options()).returning_last())
def test__build_project_sources(directory_path, module_name, module_packages, module_scripts, file_paths):
    """
    Tests whether ``build_project_sources`` works as intended.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the directory.
    module_name : `object`
        The module's name. Preferably a string.
    module_packages : `object`
        The module's packages. Preferably a list of strings.
    module_scripts : `object`
        The module's scripts. Preferably a list of strings.
    file_paths : `set<str>`
        Paths that are considered as files.
    
    Returns
    -------
    output : `None | set<str>`
    """
    def is_file_mock(path):
        nonlocal file_paths
        return path in file_paths
    
    mocked = mock_globals(
        build_project_sources,
        recursion = 4,
        is_file = is_file_mock,
    )
    
    output = mocked(directory_path, module_name, module_packages, module_scripts)
    assert_instance(output, set, nullable = True)
    return output
