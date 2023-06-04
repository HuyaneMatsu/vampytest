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
    return ''.join(style_text_into([], text, format_code))


if sys.platform == 'win32':
    def style_text_into(into, text, format_code):
        into.append(text)
        return into
    
    def style_text_block(into, format_code):
        yield

else:
    def style_text_into(into, text, format_code):
        into.append(format_code)
        into.append(text)
        into.append(STYLE_RESET)
        return into
    
    def style_text_block(into, format_code):
        into.append(format_code)
        yield
        into.append(STYLE_RESET)


set_docs(
    style_text_into,
    """
    Renders the given text with the style parts into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to add the new parts into.
    text : `str`
        Text to render with the given style.
    format_code : `str`
        Format code to style the text with.
    
    Returns
    -------
    into : `list` of `str`
    """
)


set_docs(
    style_text_block,
    """
    Renders the style into the given parts. Can be used as a block.
    
    ```py
    for _ in style_text_into(into, format_code):
        into.append(text_part)
        ...
    ```
    
    This function is an iterable generator.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to add the new parts into.
    format_code : `str`
        Format code to style the text with.
    """
)
