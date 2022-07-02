__all__ = ('EnvironmentManager', )

from .helpers import get_function_environment_type
from .default import DefaultEnvironment
from .scarletio_coroutine import ScarletioCoroutineEnvironment

from scarletio import RichAttributeErrorBaseType

DEFAULT_ENVIRONMENT_TYPES = (
    DefaultEnvironment,
    ScarletioCoroutineEnvironment,
)


class EnvironmentManager(RichAttributeErrorBaseType):
    """
    Represents an environment manager managing testing environments.
    
    Attributes
    ----------
    _environments_by_type : `dict` of (``EnvironmentType``, ``DefaultEnvironment``) items
    """
    __slots__ = ('_environments_by_type')
    
    def __new__(cls):
        """
        Creates a new environment manager.
        """
        self = object.__new__(cls)
        self._environments_by_type = {}
        return self
    
    def __repr__(self):
        """Returns the testing environment's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def get_environment_for_test(self, test):
        """
        Gets environment for the given test.
        
        Parameters
        ----------
        test : `callable`
            Test function.
        
        Returns
        -------
        environment : ``DefaultEnvironment``
        
        Raises
        ------
        NotImplementedError
        """
        type_ = get_function_environment_type(test)
        try:
            environment = self._environments_by_type[type_]
        except KeyError:
            raise NotImplementedError(
                f'No environment defined for type: {type_}'
            ) from None
        
        return environment
    
    
    def with_environment(self, environment):
        """
        Copies the environment manager with the given environment.
        
        Parameters
        ----------
        environment : ``DefaultEnvironment``
            The environment to copy self with-
        
        Returns
        -------
        new : ``EnvironmentManager``
        """
        new = self.copy()
        new._environments_by_type[environment.type] = environment
        return new
    
    
    def copy(self):
        """
        Copies the environment manager.
        
        Returns
        -------
        new : ``EnvironmentManager``
        """
        environments_by_type = self._environments_by_type.copy()
        
        new = object.__new__(type(self))
        new._environments_by_type = environments_by_type
        return new


    def populate(self):
        """
        Tries to auto populate the environment manager.
        
        Returns
        -------
        self : ``EnvironmentManager``
        """
        environments_by_type = self._environments_by_type
        
        for environment_type in DEFAULT_ENVIRONMENT_TYPES:
            type_ = environment_type.type
            if type_ not in environments_by_type:
                environments_by_type[type_] = environment_type()
        
        return self
