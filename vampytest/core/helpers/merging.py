__all__ = ()

def maybe_merge_iterables(iterable_1, iterable_2):
    """
    Merges the two maybe iterable if applicable returning a new one.
    
    Parameters
    ----------
    iterable_1 : `None`, `iterable`
        Iterable to merge.
    iterable_2 : `None`, `iterable`
        Iterable to merge.
    
    Returns
    -------
    merged : `None`, `list`
    """
    if (iterable_1 is not None) and (not iterable_1):
        iterable_1 = None
    
    if (iterable_2 is not None) and (not iterable_2):
        iterable_2 = None
    
    if iterable_1 is None:
        if iterable_2 is None:
            merged = None
        else:
            merged = [*iterable_2]
    else:
        if iterable_2 is None:
            merged = [*iterable_1]
        else:
            merged = [*iterable_1, *iterable_2]
    
    return merged


def maybe_merge_mappings(mapping_1, mapping_2):
    """
    Merges the two maybe mapping if applicable returning a new one.
    
    Parameters
    ----------
    mapping_1 : `None`, `mapping`
        Mapping to merge.
    mapping_2 : `None`, `mapping`
        Mapping to merge.
    
    Returns
    -------
    merged : `None`, `dict`
    """
    if (mapping_1 is not None) and (not mapping_1):
        mapping_1 = None
    
    if (mapping_2 is not None) and (not mapping_2):
        mapping_2 = None
    
    if mapping_1 is None:
        if mapping_2 is None:
            merged = None
        else:
            merged = {**mapping_2}
    else:
        if mapping_2 is None:
            merged = {**mapping_1}
        else:
            merged = {**mapping_1, **mapping_2}
    
    return merged
