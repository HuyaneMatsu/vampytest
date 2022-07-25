__all__ = ()

import sys

from scarletio import set_docs


class TextDecoration:
    """
    Contains the possible text decoration codes as type attributes.
    """
    reset_all = '\033[0m'
    bold = '\033[01m'
    dim = '\033[02m'


class TextBackground:
    """
    Contains the possible text background color codes as type attributes.
    """
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    dark_yellow = '\033[43m'
    blue = '\033[44m'
    dark_magenta = '\033[45m'
    teal = '\033[46m'
    light_gray = '\033[47m'
    
    reset = '\033[49m'

    gray = '\033[100m' 
    orange = '\033[101m'
    light_green = '\033[102m'
    yellow = '\033[103m'
    cyan = '\033[104m'
    pink = '\033[105m'
    light_blue = '\033[106m'
    white = '\033[107m'


class TextForeground:
    """
    Contains the possible text foreground color codes as type attributes.
    """
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    dark_yellow = '\033[33m'
    blue = '\033[34m'
    dark_magenta = '\033[35m'
    teal = '\033[36m'
    light_gray = '\033[37m'
    
    reset = '\033[39m'
    
    gray = '\033[90m'
    orange = '\033[91m'
    light_green = '\033[92m'
    yellow = '\033[93m'
    cyan = '\033[94m'
    pink = '\033[95m'
    light_blue = '\033[96m'
    white = '\033[97m'


def style_text(text, *, decoration=None, background=None, foreground=None):
    """
    Styles the given text.
    
    Parameters
    ----------
    text : `str`
        Text to render with the given style.
    decoration : `None`, `str` = `None`, Optional (Keyword only)
        ``TextDecoration``.
    background : `None`, `str` = `None`, Optional (Keyword only)
        ``TextBackground``.
    foreground : `None`, `str` = `None`, Optional (Keyword only)
        ``TextForeground``.
    
    Returns
    -------
    text : `str`
    """
    return ''.join(style_text_into(text, [], decoration=decoration, background=background, foreground=foreground))


if sys.platform == 'win32':
    def style_text_into(text, into, *, decoration=None, background=None, foreground=None):
        into.append(text)
        return into
    
else:
    def style_text_into(text, into, *, decoration=None, background=None, foreground=None):
        if (decoration is not None):
            into.append(decoration)
        
        if (background is not None):
            into.append(background)
        
        if (foreground is not None):
            into.append(foreground)
        
        into.append(text)
        
        if (decoration is not None) or (background is not None) or (foreground is not None):
            into.append(TextDecoration.reset_all)
        
        return into


set_docs(
    style_text_into,
    """
    Renders the given text with the style parts into the given list.
    
    Parameters
    ----------
    text : `str`
        Text to render with the given style.
    into : `list` of `str`
        The list of strings to add the new parts into.
    decoration : `None`, `str` = `None`, Optional (Keyword only)
        ``TextDecoration``.
    background : `None`, `str` = `None`, Optional (Keyword only)
        ``TextBackground``.
    foreground : `None`, `str` = `None`, Optional (Keyword only)
        ``TextForeground``.
    
    Returns
    -------
    into : `list` of `str`
    """
)
