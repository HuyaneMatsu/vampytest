from ...assertions import assert_instance
from ...utils import _
from ...wrappers import call_from

from ..collection import is_test_file_name


def _iter_options():
    yield '_test.py', False
    yield 'test_.py', False
    yield '_tests.py', False
    yield 'test.py', True
    yield 'tests.py', True
    yield 'test_miau.py', True
    yield 'test__miau.py', True
    yield 'tests_miau.py', False
    yield 'tests__miau.py', False
    yield 'miau_test.py', False
    yield 'miau__test.py', False
    yield 'miau_tests.py', True
    yield 'miau__tests.py', True
    yield 'miau.py', False


@_(call_from(_iter_options()).returning_last())
def test__is_test_file_name(input_value):
    """
    Tests whether ``is_test_file_name`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to test with.
    
    Returns
    -------
    output : `bool
    """
    output = is_test_file_name(input_value)
    assert_instance(output, bool)
    return output
