from ...core import _, assert_instance, call_from

from ..source_lookup import parse_git_config_file_content


def _iter_options():
    yield (
        '',
        {},
    )
    
    yield (
        (
            '[core]\n'
            '\trepositoryformatversion = 0\n'
            '\tfilemode = true\n'
            '\tbare = false\n'
            '\tlogallrefupdates = true\n'
            '[remote "origin"]\n'
            '\turl = https://orindance.party/miau\n'
            '\tfetch = +refs/heads/*:refs/remotes/origin/*\n'
            '[branch "main"]\n'
            '\tremote = origin\n'
            '\tmerge = refs/heads/main\n'
        ),
        {
            'core': {
                'repositoryformatversion': '0',
                'filemode': 'true',
                'bare': 'false',
                'logallrefupdates': 'true',
            },
            'remote': {
                'origin': {
                    'url': 'https://orindance.party/miau',
                    'fetch': '+refs/heads/*:refs/remotes/origin/*',
                },
            },
            'branch': {
                'main': {
                    'remote': 'origin',
                    'merge': 'refs/heads/main',
                },
            },            
        },
    )

    
@_(call_from(_iter_options()).returning_last())
def test__parse_git_config_file_content(content):
    """
    Tests whether ``parse_git_config_file_content`` works as intended.
    
    Parameters
    ----------
    content : `str`
        Content to parse.
    
    Returns
    -------
    output : `dict<str, ... | str>`
    """
    output = parse_git_config_file_content(content)
    assert_instance(output, dict)
    return output
