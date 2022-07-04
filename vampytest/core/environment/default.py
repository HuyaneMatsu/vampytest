__all__ = ('DefaultEnvironment',)

from ..handle import ResultState

from .constants import ENVIRONMENT_TYPE_DEFAULT

from scarletio import RichAttributeErrorBaseType


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
        test : `callable`
            The test to call
        positional_parameters : `list` of `Any`
            Positional parameters to call the test with.
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to call the test with.
        
        Returns
        -------
        result_state : ``ResultState``
            The result's product.
        """
        try:
            returned_value = test(*positional_parameters, **keyword_parameters)
        except BaseException as err:
            returned_value = None
            raised_exception = err
        else:
            raised_exception = None
        
        return ResultState(returned_value, raised_exception)
