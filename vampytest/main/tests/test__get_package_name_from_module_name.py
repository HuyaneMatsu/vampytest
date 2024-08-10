from ...core import _, assert_instance, call_from

from ..source_lookup import get_package_name_from_module_name


def _iter_options():
    yield 'orin.okuu.chen', 'orin'
    yield 'orin', 'orin'
    yield '', ''
    yield '.orin', ''


@_(call_from(_iter_options()).returning_last())
def test__get_package_name_from_module_name(module_name):
    """
    Tests whether ``get_package_name_from_module_name`` works as intended.
    
    Parameters
    ----------
    module_name : `str`
        The name of a module.
    
    Returns
    -------
    output : `str`
    """
    output = get_package_name_from_module_name(module_name)
    assert_instance(output, str)
    return output
