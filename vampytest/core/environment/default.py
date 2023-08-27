__all__ = ('DefaultEnvironment',)

from scarletio import RichAttributeErrorBaseType

from ..handling import ResultState

from .constants import ENVIRONMENT_TYPE_DEFAULT


class DefaultEnvironment(RichAttributeErrorBaseType):
    """
    Implements a default environment to call tests in.
    
    Class Attributes
    ----------------
    identifier : `int` = `ENVIRONMENT_TYPE_DEFAULT`
        Represents for which environment the test is applicable for.
    """
    __slots__ = ()
    
    identifier = ENVIRONMENT_TYPE_DEFAULT
    
    def __new__(cls):
        """
        Creates a new environment.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the environment's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def run(self, test, positional_parameters, keyword_parameters):
        """
        Runs the defined test with the given parameters.
        
        Parameters
        ----------
        test : `FunctionType`
            The test to call
        positional_parameters : `list` of `object`
            Positional parameters to call the test with.
        keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters to call the test with.
        
        Returns
        -------
        result_state : ``ResultState``
            The result's product.
        """
        try:
            returned_value = test(*positional_parameters, **keyword_parameters)
        except BaseException as raised_exception:
            return ResultState().with_raise(raised_exception)
        
        return ResultState().with_return(returned_value)
    
    
    def shutdown(self):
        """
        Stops the environment.
        
        Called on environments when testing ended and the process should shut down.
        """
        pass
