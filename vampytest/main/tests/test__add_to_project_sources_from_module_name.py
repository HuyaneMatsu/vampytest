from ...core import _, call_from, mock_globals

from ..source_lookup import add_to_project_sources_from_module_name


def _iter_options():
    # Nothing??
    yield (
        None,
        '/orin',
        None,
        {},
        None,
    )
    
    # Invalid??
    yield (
        None,
        '/orin',
        object(),
        {},
        None,
    )
    
    # cooking
    yield (
        None,
        '/orin',
        'okuu',
        {
            '/orin/okuu/__init__.py',
        },
        {
            'okuu',
        },
    )


@_(call_from(_iter_options()).returning_last())
def test__add_to_project_sources_from_module_name(project_sources, directory_path, module_name, file_paths):
    """
    Tests whether ``add_to_project_sources_from_module_name`` works as intended.
    
    Parameters
    ----------
    project_sources : `None | set<str>`
        Project sources.
    directory_path : `str`
        Path to the directory.
    module_name : `object`
        The module's name. Preferably a string.
    file_paths : `set<str>`
        Paths that are considered as files.
    
    Returns
    -------
    output : `None | set<str>`
    """
    if (project_sources is not None):
        project_sources = project_sources.copy()
    
    def is_file_mock(path):
        nonlocal file_paths
        return path in file_paths
    
    mocked = mock_globals(
        add_to_project_sources_from_module_name,
        recursion = 3,
        is_file = is_file_mock,
    )
    
    return mocked(project_sources, directory_path, module_name)
