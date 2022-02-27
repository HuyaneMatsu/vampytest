__all__ = ()

from os.path import sep as PATH_SEPARATOR


PATH_REPR_MAX_PARTS = 4
PATH_REPR_PART_PLACEHOLDER = '.'
PATH_REPR_MAX_LENGTH = 80

def get_short_path_repr(path):
    """
    Returns the short representation of the given path.
    
    Parameters
    ----------
    path : `str`
        The path to get it's short representation of.
    
    Returns
    -------
    path_repr : `str`
        The path's representation.
    """
    path_parts = path.split(PATH_SEPARATOR)
    
    path_parts_to_render = []
    
    collective_length = 0
    placeholder_count = 0
    
    # If there is first, we always add it
    if path_parts:
        path_part = path_parts.pop()
        collective_length += len(path_part)
        path_parts_to_render.append(path_part)
    
    
    # add up to our limit path parts
    for _ in range(1, PATH_REPR_MAX_PARTS):
        if not path_parts:
            break
        
        path_part = path_parts.pop()
        collective_length += len(path_part)
        if collective_length > PATH_REPR_MAX_LENGTH:
            placeholder_count += 1
            break
        
        path_parts_to_render.append(path_part)
        continue
    
    # Add empty string for every empty string in path, if path length is less than our limit
    if (collective_length <= PATH_REPR_MAX_LENGTH):
        while path_parts:
            path_part = path_parts.pop()
            if path_part:
                placeholder_count += 1
                break
            
            path_parts_to_render.append('')
            continue
    
    
    # For every not empty path part we add a placeholder
    while path_parts:
        if path_parts.pop():
            placeholder_count += 1
    
    # Build repr
    path_repr_parts = []
    
    # add placeholder
    if path_repr_parts:
        for _ in range(path_repr_parts):
            path_repr_parts.append(PATH_REPR_PART_PLACEHOLDER)
        
        path_parts_added = True
    
    else:
        path_parts_added = False
    
    # add path parts
    for path_part in reversed(path_parts_to_render):
        if path_parts_added:
            path_repr_parts.append(PATH_SEPARATOR)
        else:
            path_parts_added = True
        
        path_repr_parts.append(path_part)
    
    # join the built string
    return ''.join(path_repr_parts)
