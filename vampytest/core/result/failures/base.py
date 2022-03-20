__all__ = ('FailureBase',)

from scarletio import RichAttributeErrorBaseType


class FailureBase(RichAttributeErrorBaseType):
    """
    Base class for test failures.
    
    Attributes
    ----------
    handle : ``Handle``
        The test's handle running the test.
    """
    __slots__ = ('handle',)
    
    def __new__(cls, handle):
        """
        Base class for test failures.
        
        Parameters
        ----------
        handle : ``Handle``
            The test's handle running the test.
        """
        self = object.__new__(cls)
        self.handle = handle
        return self
    
    
    def __repr__(self):
        """Returns the test failure's representation."""
        return ''.join(['<', self.__class__.__name__, '>'])
    
   
    def get_failure_message(self):
        """
        Returns the failure message.
        
        Returns
        -------
        failure_message : `str`
        """
        return ''
