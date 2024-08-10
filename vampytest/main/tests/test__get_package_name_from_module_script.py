from ...core import _, assert_instance, call_from

from ..source_lookup import get_package_name_from_module_script


def _iter_options():
    yield 'orin = orin.__main__:__main__', 'orin'
    yield '', ''


@_(call_from(_iter_options()).returning_last())
def test__get_package_name_from_module_script(module_script):
    """
    Tests whether ``get_package_name_from_module_script`` works as intended.
    
    Parameters
    ----------
    module_script : `str`
        Module script.
    
    Returns
    -------
    output : `str`
    """
    output = get_package_name_from_module_script(module_script)
    assert_instance(output, str)
    return output
