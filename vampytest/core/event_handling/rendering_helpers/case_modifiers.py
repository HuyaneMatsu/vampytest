__all__ = ()

from reprlib import repr


def build_case_modifier(call_state):
    """
    Builds a case modifier.
    
    Parameters
    ----------
    call_state : ``CallState``
        Call state defining the case.
    
    Returns
    -------
    modifier : `str`
    """
    if call_state is None:
        return ''
    
    into = []
    name = call_state.name
    if (name is not None):
        into = _render_case_name_into(name, into)
    else:
        into = _render_case_parameters_into(call_state.positional_parameters, call_state.keyword_parameters, into)
    
    return ''.join(into)


def _render_case_parameters_into(positional_parameters, keyword_parameters, into):
    """
    Renders the result modifier parameters into the given container.
    
    Parameters
    ----------
    positional_parameters : `None | list<object>`
        Positional parameters to the the test function with.
    
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters to the call the test function with.
    
    into : `list<str>`
        String parts to render into.
    
    Returns
    ----------
    into : `list<str>`
    """
    if (positional_parameters is None) and (keyword_parameters is None):
        return into
    
    into.append('[')
    
    field_added = False
    
    if positional_parameters is not None:
        for position_parameter in positional_parameters:
            if field_added:
                into.append(', ')
            else:
                field_added = True
            
            into.append(repr(position_parameter))
            continue
    
    if (keyword_parameters is not None):
        for key in sorted(keyword_parameters.keys()):
            value = keyword_parameters[key]
            
            if field_added:
                into.append(', ')
            else:
                field_added = True
            
            into.append(key)
            into.append(' = ')
            into.append(repr(value))
    
    into.append(']')
    
    return into


def _render_case_name_into(name, into):
    """
    Renders the result modifier name into the given container.
    
    Parameters
    ----------
    name : `str`
        Name of the test case.
        
    into : `list<str>`
        String parts to render into.
    
    Returns
    ----------
    into : `list<str>`
    """
    into.append('<')
    into.append(name)
    into.append('>')
    return into
