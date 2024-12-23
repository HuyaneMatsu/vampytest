__all__ = ('ParameterMismatch',)

from scarletio import RichAttributeErrorBaseType


class ParameterMismatch(RichAttributeErrorBaseType):
    """
    Represents parameter mismatch between a test's parameters and the parameters that would been passed to it.
    
    Attributes
    ----------
    extra_keyword_parameters : `None | dict<str, object>`
        Extra keyword parameters that would been passed.
    extra_positional_parameters : `None | list<object>`
        Extra positional parameters that would been passed.
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters to call the test with.
    parameters : `list<Parameter>`
        The test's parameters.
    positional_parameters : `None | list<object>`
        Positional parameters to call the test with.
    unsatisfied_parameters : `None | list<Parameter>`
        Parameters that would not be satisfied.
    """
    __slots__ = (
        'extra_keyword_parameters', 'extra_positional_parameters', 'keyword_parameters', 'parameters',
        'positional_parameters', 'unsatisfied_parameters'
    )
    
    def __new__(
        cls,
        parameters, 
        positional_parameters,
        keyword_parameters,
        unsatisfied_parameters,
        extra_positional_parameters,
        extra_keyword_parameters,
    ):
        """
        Creates a new parameter mismatch.
        
        Parameters
        ----------
        parameters : `list<Parameter>`
            The test's parameters.
        positional_parameters : `None | list<object>`
            Positional parameters to call the test with.
        keyword_parameters : `None | dict<str, object>`
            Keyword parameters to call the test with.
        unsatisfied_parameters : `None | list<Parameter>`
            Parameters that would not be satisfied.
        extra_positional_parameters : `None | list<object>`
            Extra positional parameters that would been passed.
        extra_keyword_parameters : `None | dict<str, object>`
            Extra keyword parameters that would been passed.
        """
        self = object.__new__(cls)
        self.extra_keyword_parameters = extra_keyword_parameters
        self.extra_positional_parameters = extra_positional_parameters
        self.keyword_parameters = keyword_parameters
        self.parameters = parameters
        self.positional_parameters = positional_parameters
        self.unsatisfied_parameters = unsatisfied_parameters
        return self
    
    
    def __repr__(self):
        """Returns the parameter mismatch's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' parameters = ')
        repr_parts.append(repr(self.parameters))
        
        positional_parameters = self.positional_parameters
        if (positional_parameters is not None):
            repr_parts.append(', positional_parameters = ')
            repr_parts.append(repr(positional_parameters))
        
        keyword_parameters = self.keyword_parameters
        if (keyword_parameters is not None):
            repr_parts.append(', keyword_parameters = ')
            repr_parts.append(repr(keyword_parameters))
        
        unsatisfied_parameters = self.unsatisfied_parameters
        if (unsatisfied_parameters is not None):
            repr_parts.append(', unsatisfied_parameters = ')
            repr_parts.append(repr(unsatisfied_parameters))
            
        extra_positional_parameters = self.extra_positional_parameters
        if (extra_positional_parameters is not None):
            repr_parts.append(', extra_positional_parameters = ')
            repr_parts.append(repr(extra_positional_parameters))
        
        extra_keyword_parameters = self.extra_keyword_parameters
        if (extra_keyword_parameters is not None):
            repr_parts.append(', extra_keyword_parameters = ')
            repr_parts.append(repr(extra_keyword_parameters))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two parameter mismatches are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.extra_keyword_parameters != other.extra_keyword_parameters:
            return False
        
        if self.extra_positional_parameters != other.extra_positional_parameters:
            return False
        
        if self.keyword_parameters != other.keyword_parameters:
            return False
        
        if self.parameters != other.parameters:
            return False
        
        if self.positional_parameters != other.positional_parameters:
            return False
        
        if self.unsatisfied_parameters != other.unsatisfied_parameters:
            return False
        
        return True
