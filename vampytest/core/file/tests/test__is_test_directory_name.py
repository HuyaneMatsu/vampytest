from ...assertions import assert_instance
from ...utils import _
from ...wrappers import call_from

from ..collection import is_test_directory_name


def _iter_options():
    yield '_test', False
    yield 'test_', False
    yield '_tests', False
    yield 'test', False
    yield 'tests', True
    yield 'test_miau', True
    yield 'test__miau', True
    yield 'tests_miau', True
    yield 'tests__miau', True
    yield 'miau_test', False
    yield 'miau__test', False
    yield 'miau_tests', True
    yield 'miau__tests', True
    yield 'miau', False


@_(call_from(_iter_options()).returning_last())
def test__is_test_directory_name(input_value):
    """
    Tests whether ``is_test_directory_name`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to test with.
    
    Returns
    -------
    output : `bool
    """
    output = is_test_directory_name(input_value)
    assert_instance(output, bool)
    return output
