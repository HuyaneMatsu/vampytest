__all__ = ('WrapperEnvironment',)

from scarletio import copy_docs

from ..environment.configuration import _check_environment_type

from .wrapper_base import WrapperBase


class WrapperEnvironment(WrapperBase):
    """
    Uses a specific environment for the wrapped test.

    Attributes
    ----------
    wrapped : `None`, `object`
        The wrapped test.
    environment : ``DefaultEnvironment``
        Environment to use while running the test.
    """
    __slots__ = ('environment',)
    
    def __new__(cls, environment):
        """
        Creates a environment wrapper.
        
        Parameters
        ----------
        environment : ``DefaultEnvironment``
            Environment to use while running the test.
        
        Raises
        ------
        TypeError
            - If `environment`'s type is incorrect.
        """
        _check_environment_type(environment)
        
        self = WrapperBase.__new__(cls)
        self.environment = environment
        return self
    
    
    @copy_docs(WrapperBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} environment = {self.environment!r}'
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.environment != other.environment:
            return False
        
        return True
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        return hash(self.environment)
    
    
    @copy_docs(WrapperBase.is_ignored_when_testing)
    def is_ignored_when_testing(self):
        return True
    
    
    @copy_docs(WrapperBase.iter_environments)
    def iter_environments(self):
        yield self.environment
