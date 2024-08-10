from ...core import _, assert_eq, assert_instance, call_from

from ..source_lookup import try_get_nested


def _iter_options():
    yield (
        {
            'hey': 'mister',
        },
        (),
        {
            'hey': 'mister',
        },
    )

    yield (
        {
            'hey': 'mister',
        },
        ('orin', ),
        None,
    )

    yield (
        {
            'hey': 'mister',
        },
        ('hey', ),
        'mister',
    )

    yield (
        {
            'hey': {
                'mister' : 'sister'
            },
        },
        ('hey', ),
        {
            'mister' : 'sister'
        },
    )

    yield (
        {
            'hey': {
                'mister' : 'sister'
            },
        },
        ('hey', 'sister'),
        None,
    )

    yield (
        {
            'hey': {
                'mister' : 'sister'
            },
        },
        ('hey', 'mister'),
        'sister',
    )


@_(call_from(_iter_options()).returning_last())
def test__try_get_nested(sections, path_parts):
    """
    Tests whether ``try_get_nested`` works as intended.
    
    Parameters
    ----------
    sections : `dict<str, ... | str>`
        Sections to get from.
    path_parts : `tuple<str>`
        Path to query for.
    
    Returns
    -------
    output : `None | dict<str, ...> | str`
    """
    output = try_get_nested(sections, path_parts)
    assert_instance(output, type(None), dict, str)
    return output
