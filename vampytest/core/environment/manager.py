__all__ = ('EnvironmentManager', )

from scarletio import RichAttributeErrorBaseType

from .helpers import get_function_environment_identifier
from .default import DefaultEnvironment
from .scarletio_coroutine import ScarletioCoroutineEnvironment


DEFAULT_ENVIRONMENT_TYPES = (
    DefaultEnvironment,
    ScarletioCoroutineEnvironment,
)


class EnvironmentManager(RichAttributeErrorBaseType):
    """
    Represents an environment manager managing testing environments.
    
    Attributes
    ----------
    _environments_by_identifier : `dict` of (`int`, ``DefaultEnvironment``) items
    """
    __slots__ = ('_environments_by_identifier',)
    
    def __new__(cls):
        """
        Creates a new environment manager.
        """
        self = object.__new__(cls)
        self._environments_by_identifier = {}
        return self
    
    def __repr__(self):
        """Returns the testing environment's representation."""
        return f'<{self.__class__.__name__} environments_by_identifier = {self._environments_by_identifier!r}>'
    
    
    def get_environment_for_test(self, test):
        """
        Gets environment for the given test.
        
        Parameters
        ----------
        test : `FunctionType`
            Test function.
        
        Returns
        -------
        environment : ``DefaultEnvironment``
        
        Raises
        ------
        NotImplementedError
        """
        identifier = get_function_environment_identifier(test)
        try:
            environment = self._environments_by_identifier[identifier]
        except KeyError:
            raise NotImplementedError(
                f'No environment defined for type: {identifier}'
            ) from None
        
        return environment
    
    
    def with_environment(self, *environments):
        """
        Copies the environment manager with the given environment.
        
        Parameters
        ----------
        *environments : ``DefaultEnvironment``
            The environment to copy self with-
        
        Returns
        -------
        new : ``EnvironmentManager``
        """
        if not environments:
            return self
        
        new = self.copy()
        
        environments_by_identifier = new._environments_by_identifier
        for environment in environments:
            environments_by_identifier[environment.identifier] = environment
        
        return new
    
    
    def copy(self):
        """
        Copies the environment manager.
        
        Returns
        -------
        new : ``EnvironmentManager``
        """
        environments_by_identifier = self._environments_by_identifier.copy()
        
        new = object.__new__(type(self))
        new._environments_by_identifier = environments_by_identifier
        return new


    def populate(self):
        """
        Tries to auto populate the environment manager.
        
        Returns
        -------
        self : ``EnvironmentManager``
        """
        environments_by_identifier = self._environments_by_identifier
        
        for environment_type in DEFAULT_ENVIRONMENT_TYPES:
            identifier = environment_type.identifier
            if identifier not in environments_by_identifier:
                environments_by_identifier[identifier] = environment_type()
        
        return self
