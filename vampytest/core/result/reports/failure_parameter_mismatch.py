__all__ = ('ReportFailureParameterMismatch',)

from scarletio import copy_docs

from .base import ReportBase


class ReportFailureParameterMismatch(ReportBase):
    """
    Test failure representing parameter mismatch.
    
    Attributes
    ----------
    parameter_mismatch : ``ParameterMismatch``
        Parameter mismatch instance.
    """
    __slots__ = ('parameter_mismatch',)
    
    def __new__(cls, parameter_mismatch):
        """
        Creates a new test failure representing a bad return value.
        
        Parameters
        ----------
        parameter_mismatch : ``ParameterMismatch``
            Parameter mismatch instance.
        """
        self = object.__new__(cls)
        self.parameter_mismatch = parameter_mismatch
        return self
    
    
    @copy_docs(ReportBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' parameter_mismatch = ')
        repr_parts.append(repr(self.parameter_mismatch))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ReportBase.is_failure)
    def is_failure(self):
        return True
