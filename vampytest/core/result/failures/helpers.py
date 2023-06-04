__all__ = ()

def render_parameters_into(into, positional_parameters, keyword_parameters):
    """
    Renders the input parameters of to the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    positional_parameters : `None`, `list<object>`
        Positional parameters passed to the test.
    keyword_parameters : `None`, `dict<str, object>`
        Keyword parameters passed to the test.
    
    Returns
    -------
    into : `list` of `str`
    """
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
            into.append(' = ')
            into.append(repr(parameter_value))
    
    if not field_added:
        into.append('N/A')
    
    return into


def render_route_parts_into(into, handle):
    """
    Adds route parts into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    handle : ``Handle``
        The parent handler to get route of.
    
    Returns
    -------
    into : `list` of `str`
    """
    case = handle.case
    
    into.append(case.import_route)
    into.append('.')
    into.append(case.name)
    
    return into


def render_documentation_into(into, handle):
    """
    Adds the documentation into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to put the string parts into.
    handle : ``Handle``
        The parent handler to get it's test's documentation of.
    
    Returns
    -------
    into : `list` of `str`
    """
    documentation = handle.get_test_documentation()
    if (documentation is not None):
        into.append('\n')
        into.append(documentation)
    
    return into
