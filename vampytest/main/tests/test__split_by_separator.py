from os import sep as PATH_SEPARATOR

from ...core import _, call_from

from ..source_lookup import full_split_path


def _iter_options():
    yield PATH_SEPARATOR.join([]), []
    yield PATH_SEPARATOR.join(['', '']), []
    yield PATH_SEPARATOR.join(['', 'orin']), ['orin']
    yield PATH_SEPARATOR.join(['orin', 'cat', 'dance']), ['orin', 'cat', 'dance']
    yield PATH_SEPARATOR.join(['', 'orin', '', 'cat']), ['orin', 'cat']
    

@_(call_from(_iter_options()).returning_last())
def test__full_split_path(path):
    """
    Tests whether ``full_split_path`` works as intended.
    
    Parameters
    ----------
    path : `str`
        The path to split.
    
    Returns
    -------
    output : `list<str>`
    """
    return full_split_path(path)
