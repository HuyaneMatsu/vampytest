__all__ = ('TestFile', )

from .utils import get_short_path_repr

class TestFile:
    """
    Describes a test file.
    
    Attributes
    ----------
    path : `str`
        Absolute path to the file.
    """
    __slots__ = ('path',)
    
    def __new__(cls, path):
        """
        Creates an new test file.
        
        Parameters
        ----------
        path : `str`
            Absolute path to the file.
        """
        self = object.__new__(cls)
        self.path = path
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two test files are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.path == other.path
    
    
    def __hash__(self):
        """Returns the hash value of the test file."""
        return hash(self.path)
    
    def __repr__(self):
        """Returns the representation of a test file."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' path=')
        repr_parts.append(get_short_path_repr(self.path))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
