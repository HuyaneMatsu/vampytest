__all__ = ('CallState',)

from scarletio import RichAttributeErrorBaseType

from ..helpers.hashing import hash_dict, hash_list
from ..helpers.merging import maybe_merge_iterables, maybe_merge_mappings


class CallState(RichAttributeErrorBaseType):
    """
    Defines how the function should be called.
    
    Attributes
    ----------
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters to the call the test function with.
    
    positional_parameters : `None | list<object>`
        Positional parameters to the the test function with.
    """
    __slots__ = ('keyword_parameters', 'positional_parameters')
    
    def __new__(cls):
        """
        Creates a new calls state.
        """
        self = object.__new__(cls)
        self.keyword_parameters = None
        self.positional_parameters = None
        return self
    
    
    def __repr__(self):
        """Returns the representation of the call state."""
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        positional_parameters = self.positional_parameters
        if (positional_parameters is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' positional_parameters = ')
            repr_parts.append(repr(positional_parameters))
        
        keyword_parameters = self.keyword_parameters
        if (keyword_parameters is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' keyword_parameters = ')
            repr_parts.append(repr(keyword_parameters))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two call states are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.keyword_parameters != other.keyword_parameters:
            return False
        
        if self.positional_parameters != other.positional_parameters:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the call state's hash value."""
        hash_value = 0
        
        keyword_parameters = self.keyword_parameters
        if (keyword_parameters is not None):
            hash_value ^= 1 << 4
            hash_value ^= hash_dict(keyword_parameters)
        
        positional_parameters = self.positional_parameters
        if (positional_parameters is not None):
            hash_value ^= 1 << 8
            hash_value ^= hash_list(positional_parameters)
        
        return hash_value
    
    
    def __bool__(self):
        """Returns whether the call state holds anythings."""
        if (self.keyword_parameters is not None):
            return True
        
        if (self.positional_parameters is not None):
            return True
        
        return False
    
    
    def copy(self):
        """
        Copies the call state.
        
        Returns
        -------
        new : `instance<type<self>`
        """
        keyword_parameters = self.keyword_parameters
        if (keyword_parameters is not None):
            keyword_parameters = keyword_parameters.copy()
        
        positional_parameters = self.positional_parameters
        if (positional_parameters is not None):
            positional_parameters = positional_parameters.copy()
        
        new = object.__new__(type(self))
        new.keyword_parameters = keyword_parameters
        new.positional_parameters = positional_parameters
        return new
    
    
    def with_parameters(self, positional_parameters, keyword_parameters):
        """
        Creates a new call state with merged parameters.
        
        Parameters
        ----------
        positional_parameters : `None | list<object>`
            Positional parameters to the the test function with.
        
        keyword_parameters : `None | dict<str, object>`
            Keyword parameters to the call the test function with.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        positional_parameters = maybe_merge_iterables(self.positional_parameters, positional_parameters)
        keyword_parameters = maybe_merge_mappings(self.keyword_parameters, keyword_parameters)
        
        new = object.__new__(type(self))
        new.keyword_parameters = keyword_parameters
        new.positional_parameters = positional_parameters
        return new
