__all__ = ('ReportBase',)

from scarletio import RichAttributeErrorBaseType


class ReportBase(RichAttributeErrorBaseType):
    """
    Base type for test reports.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new report.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the report's representation."""
        return ''.join(['<', type(self).__name__, '>'])
    
    
    def is_failure(self):
        """
        Returns whether the report represents a failure.
        
        Returns
        -------
        is_failure : `bool`
        """
        return False
    
    
    def is_informal(self):
        """
        Returns whether the report is an informal report.
        
        Returns
        -------
        is_informal : `bool`
        """
        return False
