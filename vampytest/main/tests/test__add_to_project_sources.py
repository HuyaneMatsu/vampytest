from ...core import _, call_from, mock_globals

from ..source_lookup import add_to_project_sources


def _iter_options():
    # does not exist
    yield None, '/orin', 'okuu', {}, None
    
    # exists
    yield None, '/orin', 'okuu', {'/orin/okuu/__init__.py'}, {'okuu'}
    
    # already exists
    yield {'okuu'}, '/orin', 'okuu', {}, {'okuu'}

    # we have other
    yield {'chen'}, '/orin', 'okuu', {'/orin/okuu/__init__.py'}, {'chen', 'okuu'}

    # we have other, self does not exist
    yield {'chen'}, '/orin', 'okuu', {}, {'chen'}


@_(call_from(_iter_options()).returning_last())
def test__add_to_project_sources(project_sources, directory_path, name, file_paths):
    """
    Adds a project source.
    
    Parameters
    ----------
    project_sources : `None | set<str>`
        Project sources.
    directory_path : `str`
        Path to the directory.
    name : `str`
        The name of the project source to add.
    file_paths : `set<str>`
        Paths that are considered as files.
    
    Returns
    -------
    project_sources : `None | set<str>`
    """
    if (project_sources is not None):
        project_sources = project_sources.copy()
    
    def is_file_mock(path):
        nonlocal file_paths
        return path in file_paths
    
    mocked = mock_globals(
        add_to_project_sources,
        recursion = 2,
        is_file = is_file_mock,
    )
    
    return mocked(project_sources, directory_path, name)
