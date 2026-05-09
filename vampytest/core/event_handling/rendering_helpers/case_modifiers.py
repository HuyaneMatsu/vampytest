__all__ = ()

from reprlib import repr as short_repr


def iter_build_case_modifier(call_state):
    """
    Builds a case modifier.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    call_state : ``CallState``
        Call state defining the case.
    
    Yields
    ------
    part : `str`
    """
    if call_state is None:
        return
    
    name = call_state.name
    if (name is not None):
        yield from _iter_build_case_name_parts(name)
    else:
        yield from _iter_build_case_parameters(call_state.positional_parameters, call_state.keyword_parameters)


def _iter_build_case_parameters(positional_parameters, keyword_parameters):
    """
    Renders the result modifier parameters into the given container.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    positional_parameters : `None | list<object>`
        Positional parameters to the the test function with.
    
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters to the call the test function with.
    
    Yields
    ------
    part : `str`
    """
    if (positional_parameters is None) and (keyword_parameters is None):
        return
    
    yield '['
    
    field_added = False
    
    if positional_parameters is not None:
        for position_parameter in positional_parameters:
            if field_added:
                yield ', '
            else:
                field_added = True
            
            yield short_repr(position_parameter)
            continue
    
    if (keyword_parameters is not None):
        for key in sorted(keyword_parameters.keys()):
            value = keyword_parameters[key]
            
            if field_added:
                yield ', '
            else:
                field_added = True
            
            yield key
            yield ' = '
            yield short_repr(value)
    
    yield ']'


def _iter_build_case_name_parts(name):
    """
    Renders the result modifier name into the given container.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        Name of the test case.
    
    Yields
    ------
    part : `str`
    """
    yield '<'
    yield name
    yield '>'
