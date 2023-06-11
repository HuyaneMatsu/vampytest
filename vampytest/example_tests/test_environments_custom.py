from vampytest import DefaultEnvironment, ResultState, in_environment, returning
from vampytest.core.environment.constants import ENVIRONMENT_TYPE_GENERATOR


# We create an environment that unpacks generators into a list
class GenerativeReturnTestEnvironment(DefaultEnvironment):
    __slots__ = ()
    
    # Define that this environment is only applicable for generators and propagates the tests' result like that
    identifier = ENVIRONMENT_TYPE_GENERATOR
    
    # Run is called to run the test with the given parameters and excepts it to return a `ResultState`
    def run(self, test, positional_parameters, keyword_parameters):
        try:
            returned_value = [*test(*positional_parameters, **keyword_parameters)]
        except BaseException as err:
            returned_value = None
            raised_exception = err
        else:
            raised_exception = None
        
        return ResultState(returned_value, raised_exception)
    
    # Shutdown is run when we do not need this environment anymore. Can be useful when using global environments.
    def shutdown(self):
        pass


@in_environment(GenerativeReturnTestEnvironment())
@returning([1, 2])
def test_generator_in_environment():
    yield 1
    yield 2
