__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES, get_token_type_and_repr_mode_for_variable


def _produce_representation_exception(value_type, exception_type):
    """
    Produces an exception occurring while getting the representation of an.
    
    This function is a generator.
    
    Parameters
    ----------
    value_type : `type`
        The value's type that failed to be represented.
    
    exception_type : `type<BaseException>`
        The occurred exception's type.
    
    Yields
    ------
    token_type_and_part : `(int, str)`
    """
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'repr'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, value_type.__name__
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TRACE_TITLE, 'due to'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    token_type, use_name = get_token_type_and_repr_mode_for_variable(exception_type)
    yield token_type, exception_type.__name__


def _produce_assignment_representation_maybe_exception(
    parameter_name, token_type, value_type, representation, representation_exception_type
):
    """
    Produces an assignment with the given representation that may have been failed to be represented.
    
    Parameters
    ----------
    parameter_name : `None | str`
        The parameter's name.
    
    token_type : `int`
        Token type to yield.
    
    representation : `None | str`
        The object's representation. If passed as `None`, it is assumed, that it was failed to be represented.
    
    representation_exception_type : `None | type<BaseException>`
        The occurred exception's type.
    
    Yields
    ------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_variable_assignation(parameter_name)
    if (representation is None):
        yield from _produce_representation_exception(
            value_type, representation_exception_type
        )
    else:
        yield token_type, representation
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


def _produce_assignment_representation_with_mismatch(
    parameter_name, match_token_type, mismatch_token_type, representation, matching_blocks, start_index
):
    """
    Produces assignment representation with mismatch.
    
    Parameters
    ----------
    parameter_name : `None | str`
        The parameter's name.
    
    match_token_type : `int`
        Token type to yield for matches.
    
    mismatch_token_type : `int`
        Token type to yield for mismatches.
    
    representation : `str`
        The object's representation.
    
    matching_blocks : `list<Match>>`
        Matching blocks between two representations.
    
    start_index : `int`
        The elements' index in `Match`-s that represent where a matching block starts. Can be either `0` or `1`.
    
    Yields
    ------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_variable_assignation(parameter_name)
    matching_block_end = 0
    
    for matching_block in matching_blocks:
        matching_block_start = matching_block[start_index]
        matching_block_length = matching_block[2]
        
        if matching_block_end != matching_block_start:
            yield mismatch_token_type, representation[matching_block_end : matching_block_start]
        
        matching_block_end = matching_block_start + matching_block_length
        if matching_block_length:
            yield match_token_type, representation[matching_block_start : matching_block_end]
    
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


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
        yield from _produce_representation_exception(type(value), type(exception))
    else:
        yield token_type, representation


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
