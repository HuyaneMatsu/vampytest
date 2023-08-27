__all__ = ('ReportOutput',)

from scarletio import copy_docs

from .base import ReportBase


class ReportOutput(ReportBase):
    """
    Reports output of a test.
    
    Attributes
    ----------
    str : `bool`
    """
    __slots__ = ('output',)
    
    def __new__(cls, output):
        """
        Creates a new report.
        """
        self =  object.__new__(cls)
        self.output = output
        return self
    
    
    def __repr__(self):
        """Returns the report's representation."""
        return ''.join(['<', self.__class__.__name__, ' output = ', repr(self.output), '>'])
    
    
    @copy_docs(ReportBase.is_informal)
    def is_informal(self):
        return True
