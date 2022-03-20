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
    added_field_count = 0
    was_last_field_last = False
    was_last_followed_by_empty = False
    
    
    while path_parts:
        path_part = path_parts.pop()
        if (collective_length < PATH_REPR_MAX_LENGTH) and (added_field_count < PATH_REPR_MAX_PARTS):
            new_length = collective_length + len(path_part)
            if new_length > PATH_REPR_MAX_LENGTH:
                if added_field_count == 0:
                    path_parts_to_render.append(path_part)
                else:
                    path_parts_to_render.append(PATH_SEPARATOR)
                    path_parts_to_render.append('.')
                was_last_field_last = True
            
            else:
                if added_field_count:
                    path_parts_to_render.append(PATH_SEPARATOR)
                
                added_field_count += 1
                if (added_field_count == PATH_REPR_MAX_PARTS):
                    was_last_field_last = True
                
                path_parts_to_render.append(path_part)
            
            collective_length = new_length
        
        else:
            if was_last_field_last:
                was_last_field_last = False
                
                path_parts_to_render.append(PATH_SEPARATOR)
                
                if path_part:
                    path_parts_to_render.append('.')
                else:
                    was_last_followed_by_empty = True
            else:
                if was_last_followed_by_empty:
                    was_last_followed_by_empty = False
                    path_parts_to_render.append(PATH_SEPARATOR)
                    
                if path_part:
                    path_parts_to_render.append('.')
    
    
    path_parts_to_render.reverse()
    return ''.join(path_parts_to_render)
