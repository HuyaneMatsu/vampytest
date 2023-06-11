from vampytest import DefaultEnvironment, ResultState, in_environment, returning, set_file_environment
from vampytest.core.environment.constants import ENVIRONMENT_TYPE_DEFAULT, ENVIRONMENT_TYPE_GENERATOR


class GenerativeReturnTestEnvironment(DefaultEnvironment):
    __slots__ = ()
    
    identifier = ENVIRONMENT_TYPE_GENERATOR
    
    def run(self, test, positional_parameters, keyword_parameters):
        try:
            returned_value = [*test(*positional_parameters, **keyword_parameters)]
        except BaseException as err:
            returned_value = None
            raised_exception = err
        else:
            raised_exception = None
        
        return ResultState(returned_value, raised_exception)


class PlusOneTestEnvironment(DefaultEnvironment):
    __slots__ = ()
    identifier = ENVIRONMENT_TYPE_DEFAULT
    
    def run(self, test, positional_parameters, keyword_parameters):
        try:
            returned_value = test(*positional_parameters, **keyword_parameters) + 1
        except BaseException as err:
            returned_value = None
            raised_exception = err
        else:
            raised_exception = None
        
        return ResultState(returned_value, raised_exception)


@in_environment(PlusOneTestEnvironment())
@returning(1)
def test_test_specific_environment():
    """
    Tests the directly registered environment.
    """
    return 0


set_file_environment(GenerativeReturnTestEnvironment())

@returning([1, 2])
def test_file_specific_environment():
    """
    Tests the file specific environment.
    """
    yield 1
    yield 2
