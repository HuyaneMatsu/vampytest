from ...core import _, assert_instance, call_from

from ..source_lookup import build_project_sources


def _iter_options():
    yield None, None, None
    yield object(), object(), None
    yield 'vampy', None, {'vampy'}
    yield None, ['vampy.eyes'], {'vampy'}
    yield 'eyes', ['vampy.eyes'], {'vampy'}
    yield None, ['vampy.test', 'Remilia', 'Sakuya.knife.blade'], {'vampy', 'Remilia', 'Sakuya'}


@_(call_from(_iter_options()).returning_last())
def test__build_project_sources(module_name, module_packages):
    """
    Tests whether ``build_project_sources`` works as intended.
    
    Parameters
    ----------
    module_name : `object`
        The module's name. Preferably a string.
    module_packages : `object`
        The module's packages. Preferably a list of strings.
    
    Returns
    -------
    output : `None | set<str>`
    """
    output = build_project_sources(module_name, module_packages)
    assert_instance(output, set, nullable = True)
    return output
