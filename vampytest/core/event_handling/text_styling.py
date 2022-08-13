__all__ = ()

import sys

from scarletio import create_ansi_format_code, set_docs


STYLE_RESET = create_ansi_format_code()

def style_text(text, format_code):
    """
    Styles the given text.
    
    Parameters
    ----------
    text : `str`
        Text to render with the given style.
    format_code : `str`
        Format code to style the text with.
    
    Returns
    -------
    text : `str`
    """
    return ''.join(style_text_into(text, [], format_code))


if sys.platform == 'win32':
    def style_text_into(text, into, format_code):
        into.append(text)
        return into
    
else:
    def style_text_into(text, into, format_code):
        into.append(format_code)
        into.append(text)
        into.append(STYLE_RESET)
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
    format_code : `str`
        Format code to style the text with.
    
    Returns
    -------
    into : `list` of `str`
    """
)
