__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES, get_token_type_and_repr_mode_for_variable


def _produce_value_representation(value):
    """
    Gets the value's representation.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    value : `object`
        Value to get representation of.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    token_type, use_name = get_token_type_and_repr_mode_for_variable(value)
    if use_name:
        yield token_type, value.__name__
        return
    
    try:
        representation = repr(value)
    except Exception as exception:
        retrieved_exception_type = type(exception)
    else:
        yield token_type, representation
        return
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'repr'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, type(value).__name__
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_TITLE, 'due to'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    token_type, use_name = get_token_type_and_repr_mode_for_variable(retrieved_exception_type)
    yield token_type, retrieved_exception_type.__name__


def _produce_assignation():
    """
    Produces assignation for highlighting.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '='
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    

def _produce_variable_assignation(variable_name):
    """
    Produces variable assignation for highlighting.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, variable_name
    yield from _produce_assignation()


def _produce_parameter_representation(parameter_name, parameter_value):
    """
    Renders the given parameter into the given list of strings.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    parameter_name : `None | str`
        The parameter's name.
    
    parameter_value : `object`
        The parameter's value.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    if (parameter_name is not None):
        yield from _produce_variable_assignation(parameter_name)
    
    yield from _produce_value_representation(parameter_value)
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


def _parameter_representation_sort_key(produced):
    """
    Sorter key for parameter representations.
    
    Parameters
    ----------
    produced : `tuple<(int, str)>`
        The produced representation.
    
    Returns
    -------
    key : `(int, str)`
    """
    return (len(produced), produced[0][1])


def _produce_types_parameter_representation(parameter_name, types):
    """
    Renders the given types parameter into the given list of strings.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    parameter_name : `None | str`
        The parameter's name.
    
    types : `set<type | instance<type>>`
        The parameter's value.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    if (parameter_name is not None):
        yield from _produce_variable_assignation(parameter_name)
    
    representations = sorted(
        ((*_produce_value_representation(type_),) for type_ in types),
        key = _parameter_representation_sort_key,
    )
    length = len(representations)
    if length:
        index = 0
        
        while True:
            yield from representations[index]
            
            index += 1
            if index == length:
                break
            
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ',',
            yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
            continue
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


def _produce_bool_non_default(parameter_name, parameter_value, default):
    """
    Renders a value value only if its true.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    parameter_name : `None | str`
        The parameter's name.
    
    parameter_value : `bool`
        The parameter's value.
    
    default : `bool`
        Default value.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    if parameter_value != default:
        yield from _produce_parameter_representation(parameter_name, parameter_value)
