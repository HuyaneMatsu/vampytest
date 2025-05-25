__all__ = ()

from os import get_terminal_size

from scarletio import HIGHLIGHT_TOKEN_TYPES

from ..default_output_writer import DEFAULT_BREAK_LINE_LENGTH

from .parameter_rendering import _produce_parameter_representation


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


def produce_test_header(token_type, title, path_parts, name, documentation_lines, call_state):
    """
    Renders the test's position into the given list.
    
    This functions is an iterable generator.
    
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
    
    call_state : ``None | CallState``
        Call state to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # title
    yield token_type, title
    yield token_type, ' at:'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    
    # location
    length = len(path_parts)
    if length:
        index = 0
        while True:
            part = path_parts[index]
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_LOCATION_PATH, part
            
            index += 1
            if index == length:
                break
            
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE, '.'
            continue
        
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ':'
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, name
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    
    # documentation
    if (documentation_lines is not None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        
        for line in documentation_lines:
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_CONSOLE_MARKER_PREFIX, '>'
            if line:
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_STRING, line
            
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
            continue
    
    # call_state (parameters)
    if (call_state is not None):
        case_name = call_state.name
        if (case_name is not None):
            yield from produce_case_name_section(case_name)
        
        positional_parameters = call_state.positional_parameters
        keyword_parameters = call_state.keyword_parameters
        
        if (positional_parameters is not None) or (keyword_parameters is not None):
            yield from produce_parameters_section('Parameters:', positional_parameters, keyword_parameters)


def produce_case_name_section(name):
    """
    Renders the test case's name into the given list.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        The test case's name.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, 'Named:'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, name
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


def produce_parameters_section(title, positional_parameters, keyword_parameters):
    """
    Renders the input parameters of to the given list.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    title : `str`
        Section title.
    
    positional_parameters : `None | list<object>`
        Positional parameters passed to the test.
    
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters passed to the test.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # render title
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_TITLE, title
    
    # render body
    if (positional_parameters is None) and (keyword_parameters is None):
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_NON_SPACE_UNIDENTIFIED, 'N/A'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
    
    else:
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'
        
        if (positional_parameters is not None):
            for parameter_value in positional_parameters:
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, '    '
                yield from _produce_parameter_representation(None, parameter_value)
        
        
        if (keyword_parameters is not None):
            for (parameter_name, parameter_value) in keyword_parameters.items():
                yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, '    '
                yield from _produce_parameter_representation(parameter_name, parameter_value)
