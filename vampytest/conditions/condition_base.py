__all__ = ('ConditionBase',)

class ConditionBase:
    """
    Base class for conditions.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new condition.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the condition's representation."""
        return f'<{self.__class__.__name__}>'
