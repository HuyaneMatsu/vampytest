__all__ = ()

from reprlib import repr


def build_result_modifier_parameters(modifier_parameters):
    """
    Builds result modifier parameters. If `modifier_parameters` is `None` the output will be an an empty string.
    
    Parameters
    ----------
    modifier_parameters : `None | (None | list<object>, None | dict<str, object>)`
        Positional - keyword parameters pair.
    
    Returns
    -------
    built_value : `str`
    """
    return ''.join(render_result_modifier_parameters(modifier_parameters, []))


def render_result_modifier_parameters(modifier_parameters, into):
    """
    Renders the result modifier parameters into the given container.
    
    Parameters
    ----------
    modifier_parameters : `None | (None | list<object>, None | dict<str, object>)`
        Positional - keyword parameters pair.
    
    into : `list<str>`
        String parts to render into.
    
    Returns
    ----------
    into : `list<str>`
    """
    if modifier_parameters is None:
        return into
    
    position_parameters, keyword_parameters = modifier_parameters
    if (position_parameters is None) and (keyword_parameters is None):
        return into
    
    into.append('[')
    
    field_added = False
    
    if position_parameters is not None:
        for position_parameter in position_parameters:
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
