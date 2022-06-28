__all__ = ()

def render_parameters_into(call_state, into):
    """
    Renders the input parameters of to the given list.
    
    Parameters
    ----------
    call_state : ``CallState``
        Call state containing the parameters.
    into : `list` of `str`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list` of `str`
    """
    positional_parameters = call_state.positional_parameters
    keyword_parameters = call_state.keyword_parameters
    
    field_added = False
    
    if (positional_parameters is not None):
        for parameter_value in positional_parameters:
            if field_added:
                into.append(', ')
            else:
                field_added = True
            
            into.append(repr(parameter_value))
    
    
    if (keyword_parameters is not None):
        for (parameter_name, parameter_value) in keyword_parameters.items():
            if field_added:
                into.append(', ')
            else:
                field_added = True
            
            into.append(parameter_name)
            into.append('=')
            into.append(repr(parameter_value))
    
    if not field_added:
        into.append('N/A')
    
    return into


def add_route_parts_into(handle, into):
    """
    Adds route parts into the given list.
    
    Parameters
    ----------
    failure : ``Handle``
        The parent handler to get route of.
    into : `list` of `str`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list` of `str`
    """
    case = handle.case
    
    into.append(case.import_route)
    into.append('.')
    into.append(case.name)
    
    return into


def add_documentation_into(handle, into):
    """
    Adds the documentation into the given list.
    
    Parameters
    ----------
    failure : ``Handle``
        The parent handler to get it's test's documentation of.
    into : `list` of `str`
        A list to put the string parts into.
    
    Returns
    -------
    into : `list` of `str`
    """
    documentation = handle.get_test_documentation()
    if (documentation is not None):
        into.append('\n')
        into.append(documentation)
    
    return into
