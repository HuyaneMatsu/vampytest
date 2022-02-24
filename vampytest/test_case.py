__all__ = ('TestCase', )

class TestCase:
    """
    
    Attributes
    ----------
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        
        Parameters
        ----------
        """
        self = object.__new__(cls)
        
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two test cases are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return False
    
    
    def __hash__(self):
        """Returns the test case's hash value."""
        hash_value = 0
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the test case's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def invoke(self):
        """
        Invokes the test case.
        """
        pass
