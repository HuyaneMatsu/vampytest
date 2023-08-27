__all__ = ('ResultState',)

from scarletio import RichAttributeErrorBaseType, export

from ..helpers.hashing import hash_object


RESULT_STATE_MODE_NONE = 0
RESULT_STATE_MODE_RETURN = 1
RESULT_STATE_MODE_RAISE = 2


@export
class ResultState(RichAttributeErrorBaseType):
    """
    Represents a test's output.
    
    Attributes
    ----------
    mode : `int`
        The result's mode.
    result : `None`, `object`
        The resulted value.
    """
    __slots__ = ('mode', 'result')
    
    def __new__(cls):
        """
        Creates a new result state.
        """
        self = object.__new__(cls)
        self.mode = RESULT_STATE_MODE_NONE
        self.result = None
        return self
    
    
    def __repr__(self):
        """Returns the representation of the result state."""
        repr_parts = ['<', self.__class__.__name__]
        
        mode = self.mode
        if mode == RESULT_STATE_MODE_NONE:
            field_name = None
        elif mode == RESULT_STATE_MODE_RETURN:
            field_name = 'returned_value'
        elif mode == RESULT_STATE_MODE_RAISE:
            field_name = 'raised_exception'
        else:
            field_name = None
        
        if (field_name is not None):
            repr_parts.append(' ')
            repr_parts.append(field_name)
            repr_parts.append(' = ')
            repr_parts.append(repr(self.result))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two result states are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.mode != other.mode:
            return False
        
        if self.result != other.result:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the result state's hash value."""
        hash_value = 0
        
        hash_value ^= self.mode
        
        result = self.result
        if (result is not None):
            hash_value ^= hash_object(result)
        
        return hash_value
    
    
    def __bool__(self):
        """Returns whether the result state holds anythings."""
        return self.mode != RESULT_STATE_MODE_NONE
    
    
    def copy(self):
        """
        Copies the result state.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.mode = self.mode
        new.result = self.result
        return new
    
    
    def with_return(self, returned_value):
        """
        Creates a new call state overwriting the old one.
        
        Parameters
        ----------
        returned_value : `None`, `object`
            The returned value by the test.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.mode = RESULT_STATE_MODE_RETURN
        new.result = returned_value
        return new
    
    
    def with_raise(self, raised_exception):
        """
        Creates a new call state overwriting the old one.
        
        Parameters
        ----------
        raised_exception : `BaseException`
            The raised exception by the test.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        RuntimeError
            - Raised exception can only be `BaseException` instance.
        """
        if not isinstance(raised_exception, BaseException):
            raise TypeError(
                f'`raised_exception` can only be `{BaseException.__name__}` instance. '
                f'Got {raised_exception.__class__.__name__}; {raised_exception!r}.'
            )
        
        new = object.__new__(type(self))
        new.mode = RESULT_STATE_MODE_RAISE
        new.result = raised_exception
        return new
    
    
    def is_return(self):
        """
        Returns whether the result is a return value.
        
        Returns
        -------
        is_return : `bool`
        """
        return self.mode == RESULT_STATE_MODE_RETURN
    
    
    def is_raise(self):
        """
        Returns whether the result is a raised exception.
        
        Returns
        -------
        is_raise : `bool`
        """
        return self.mode == RESULT_STATE_MODE_RAISE
