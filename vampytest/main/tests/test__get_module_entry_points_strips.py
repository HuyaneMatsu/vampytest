from ...core import _, call_from

from ..source_lookup import get_module_entry_points_strips


def _iter_options():
    yield (
        None,
        None,
    )
    
    yield (
        object(),
        None,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'console_scripts': 123,
        },
        123,
    )
    
    yield (
        {
            'console_scripts': [            
                'vampytest = vampytest.__main__:__main__',
            ],
        },
        [            
            'vampytest = vampytest.__main__:__main__',
        ],
    )


@_(call_from(_iter_options()).returning_last())
def test__get_module_entry_points_strips(module_entry_points):
    """
    Tests whether ``get_module_entry_points_strips`` works as intended.
    
    Parameters
    ----------
    module_entry_points : `object`
        Module entry points to get scripts from.
    
    Returns
    -------
    output : `object`
    """
    return get_module_entry_points_strips(module_entry_points)
