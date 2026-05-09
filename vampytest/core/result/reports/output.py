__all__ = ('ReportOutput',)

from scarletio import copy_docs

from .base import ReportBase


class ReportOutput(ReportBase):
    """
    Reports output of a test.
    
    Attributes
    ----------
    output : `str`
        Test output.
    """
    __slots__ = ('output',)
    
    def __new__(cls, output):
        """
        Creates a new report.
        
        Attributes
        ----------
        output : `str`
            Test output.
        """
        self =  object.__new__(cls)
        self.output = output
        return self
    
    
    def __repr__(self):
        """Returns the report's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # output
        repr_parts.append(' output = ')
        repr_parts.append(repr(self.output))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ReportBase.is_informal)
    def is_informal(self):
        return True
