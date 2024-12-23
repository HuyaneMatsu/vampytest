__all__ = ()

from os import get_terminal_size

from scarletio import HIGHLIGHT_TOKEN_TYPES, add_highlighted_part_into

from ..default_output_writer import DEFAULT_BREAK_LINE_LENGTH

from .parameter_rendering import _render_parameter_representation_into


def create_break(character):
    """
    Creates a break with the given character.
    
    Parameters
    ----------
    character : `str`
        The character to create the break from.
    
    Returns
    -------
    break : `str`
    """
    try:
        terminal_size = get_terminal_size()
    except OSError:
        break_line_length = DEFAULT_BREAK_LINE_LENGTH
    else:
        break_line_length = terminal_size.columns

    return character * break_line_length


def render_test_header_into(token_type, title, path_parts, name, documentation_lines, call_state, highlighter, into):
    """
    Renders the test's position into the given list.
    
    Parameters
    ----------
    token_type : `int`
        Token type identifier.
    
    title : `str`
        The title to add.
    
    path_parts : `tuple<str>`
        Path parts from the imported file.
    
    name : `str`
        The test's name.
    
    documentation_lines : `None | list<str>`
        Lines of the test's documentation.
    
    call_state : `None | CallState`
        Call state to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list<str>`
    """
    # title
    into = add_highlighted_part_into(token_type, title + ' at:', highlighter, into)
    into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, into)
    
    # location
    length = len(path_parts)
    if length:
        index = 0
        while True:
            part = path_parts[index]
            into = add_highlighted_part_into(
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_LOCATION_PATH, part, highlighter, into
            )
            index += 1
            if index == length:
                break
            
            into = add_highlighted_part_into(
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE, '.', highlighter, into
            )
            continue
        
        into = add_highlighted_part_into(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ':', highlighter, into
        )
    
    into = add_highlighted_part_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, name, highlighter, into
    )
    into.append('\n')
    
    # documentation
    if (documentation_lines is not None):
        into.append('\n')
        
        for line in documentation_lines:
            into = add_highlighted_part_into(
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX, '>', highlighter, into
            )
            if line:
                into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, into)
                into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_STRING, line, highlighter, into)
            
            into.append('\n')
            continue
    
    # call_state (parameters)
    if (call_state is not None) and call_state:
        into = render_parameters_section_into(
            'Parameters:',
            call_state.positional_parameters,
            call_state.keyword_parameters,
            highlighter,
            into,
        )
    
    return into


def render_parameters_section_into(
    title, positional_parameters, keyword_parameters, highlighter, into
):
    """
    Renders the input parameters of to the given list.
    
    Parameters
    ----------
    title : `str`
        Section title.
    
    positional_parameters : `None | list<object>`
        Positional parameters passed to the test.
    
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters passed to the test.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list<str>`
    """
    # render title
    into.append('\n')
    into = add_highlighted_part_into(
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, title, highlighter, into
    )
    
    # render body
    if (positional_parameters is None) and (keyword_parameters is None):
        into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, into)
        into = add_highlighted_part_into(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_NON_SPACE_UNIDENTIFIED, 'N/A', highlighter, into
        )
        into.append('\n')
    
    else:
        into.append('\n')
        
        if (positional_parameters is not None):
            for parameter_value in positional_parameters:
                into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, '    ', highlighter, into)
                into = _render_parameter_representation_into(None, parameter_value, highlighter, into)
        
        
        if (keyword_parameters is not None):
            for (parameter_name, parameter_value) in keyword_parameters.items():
                into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, '    ', highlighter, into)
                into = _render_parameter_representation_into(parameter_name, parameter_value, highlighter, into)
    
    return into
