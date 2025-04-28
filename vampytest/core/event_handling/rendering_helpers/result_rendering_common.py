__all__ = ()

from os import get_terminal_size

from scarletio import HIGHLIGHT_TOKEN_TYPES

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


def render_test_header_into(
    token_type, title, path_parts, name, documentation_lines, call_state, highlight_streamer, into
):
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
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list<str>`
    """
    # title
    into.extend(highlight_streamer.asend((
        token_type,
        title + ' at:',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
        ' ',
    )))
    
    # location
    length = len(path_parts)
    if length:
        index = 0
        while True:
            part = path_parts[index]
            
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_LOCATION_PATH,
                part,
            )))
            index += 1
            if index == length:
                break
            
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE,
                '.',
            )))
            continue
        
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION,
            ':',
        )))
    
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION,
        name,
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    
    # documentation
    if (documentation_lines is not None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        
        for line in documentation_lines:
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX,
                '>',
            )))
            if line:
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
                    ' ',
                )))
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_STRING,
                    line,
                )))
            
            into.extend(highlight_streamer.asend((
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
                '\n',
            )))
            continue
    
    # call_state (parameters)
    if (call_state is not None):
        case_name = call_state.name
        if (case_name is not None):
            into = render_case_name_section_into(case_name, highlight_streamer, into)
        
        positional_parameters = call_state.positional_parameters
        keyword_parameters = call_state.keyword_parameters
        
        if (positional_parameters is not None) or (keyword_parameters is not None):
            into = render_parameters_section_into(
                'Parameters:',
                positional_parameters,
                keyword_parameters,
                highlight_streamer,
                into,
            )
    
    return into


def render_case_name_section_into(name, highlight_streamer, into):
    """
    Renders the test case's name into the given list.
    
    Parameters
    ----------
    name : `str`
        The test case's name.
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list<str>`
    """
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE,
        'Named:',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
        ' ',
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE,
        name,
    )))
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    return into


def render_parameters_section_into(
    title, positional_parameters, keyword_parameters, highlight_streamer, into
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
    
    highlight_streamer : `CoroutineGeneratorType`
        Highlight streamer to highlight the produced tokens.
    
    into : `list<str>`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list<str>`
    """
    # render title
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
        '\n',
    )))
    
    into.extend(highlight_streamer.asend((
        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE,
        title,
    )))
    
    # render body
    if (positional_parameters is None) and (keyword_parameters is None):
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
            ' ',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_NON_SPACE_UNIDENTIFIED,
            'N/A',
        )))
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
    
    else:
        into.extend(highlight_streamer.asend((
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK,
            '\n',
        )))
        
        if (positional_parameters is not None):
            for parameter_value in positional_parameters:
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
                    '    ',
                )))
                into = _render_parameter_representation_into(None, parameter_value, highlight_streamer, into)
        
        
        if (keyword_parameters is not None):
            for (parameter_name, parameter_value) in keyword_parameters.items():
                into.extend(highlight_streamer.asend((
                    HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE,
                    '    ',
                )))
                into = _render_parameter_representation_into(parameter_name, parameter_value, highlight_streamer, into)
    
    return into
