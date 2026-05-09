from ...core import _, call_from

from ..source_lookup import get_target_path_from_parameters


def _iter_options():
    yield [], 0, (None, 0)
    yield ['-koishi'], 0, (None, 0)
    yield ['koishi'], 1, (None, 1)
    yield ['koishi'], 0, ('koishi', 1)


@_(call_from(_iter_options()).returning_last())
def test__get_target_path_from_parameters(parameters, index):
    """
    Tests whether ``get_target_path_from_parameters`` works as intended.
    
    Parameters
    ----------
    parameters : `list<str>`
        System parameters usually.
    index : `int`
        The index to read from.
    
    Returns
    -------
    output : `(str, int)`
    """
    return get_target_path_from_parameters(parameters, index)
