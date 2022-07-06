__all__ = ('CallState', 'ResultState', 'Handle',)

import gc, reprlib

from .helpers import hash_dict, hash_list, hash_object, maybe_merge_iterables, maybe_merge_mappings

from scarletio import RichAttributeErrorBaseType, include


Result = include('Result')
AssertionException = include('AssertionException')


class CallState(RichAttributeErrorBaseType):
    """
    Defines how the function should be called.
    
    Attributes
    ----------
    keyword_parameters : `None`, `dict` of (`str`, `Any`) items
        Keyword parameters to the call the test function with.
    positional_parameters : `None`, `list` of `Any`
        Positional parameters to the the test function with.
    """
    __slots__ = ('keyword_parameters', 'positional_parameters')
    
    def __new__(cls):
        """
        Creates a new calls state.
        """
        self = object.__new__(cls)
        self.keyword_parameters = None
        self.positional_parameters = None
        return self
    
    
    def __repr__(self):
        """Returns the representation of the call state."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        positional_parameters = self.positional_parameters
        if (positional_parameters is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' positional_parameters')
            repr_parts.append(repr(positional_parameters))
        
        keyword_parameters = self.keyword_parameters
        if (keyword_parameters is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' keyword_parameters')
            repr_parts.append(repr(keyword_parameters))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two call states are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.keyword_parameters != other.keyword_parameters:
            return False
        
        if self.positional_parameters != other.positional_parameters:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the call state's hash value."""
        hash_value = 0
        
        keyword_parameters = self.keyword_parameters
        if (keyword_parameters is not None):
            hash_value ^= 1 << 4
            hash_value ^= hash_dict(keyword_parameters)
        
        positional_parameters = self.positional_parameters
        if (positional_parameters is not None):
            hash_value ^= 1 << 8
            hash_value ^= hash_list(positional_parameters)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the call state.
        
        Returns
        -------
        new : ``CallState``
        """
        keyword_parameters = self.keyword_parameters
        if (keyword_parameters is not None):
            keyword_parameters = keyword_parameters.copy()
        
        positional_parameters = self.positional_parameters
        if (positional_parameters is not None):
            positional_parameters = positional_parameters.copy()
        
        new = object.__new__(type(self))
        new.keyword_parameters = keyword_parameters
        new.positional_parameters = positional_parameters
        return new
    
    
    def with_parameters(self, positional_parameters, keyword_parameters):
        """
        Creates a new call state with merged parameters.
        
        Parameters
        ----------
        positional_parameters : `None`, `list` of `Any`
            Positional parameters to the the test function with.
        keyword_parameters : `None`, `dict` of (`str`, `Any`) items
            Keyword parameters to the call the test function with.
        
        Returns
        -------
        new : ``CallState``
        """
        positional_parameters = maybe_merge_iterables(self.positional_parameters, positional_parameters)
        keyword_parameters = maybe_merge_mappings(self.keyword_parameters, keyword_parameters)
        
        new = object.__new__(type(self))
        new.keyword_parameters = keyword_parameters
        new.positional_parameters = positional_parameters
        return new
    
    
    def __bool__(self):
        """Returns whether the call state holds anythings."""
        if (self.keyword_parameters is not None):
            return True
        
        if (self.positional_parameters is not None):
            return True
        
        return False


class ResultState(RichAttributeErrorBaseType):
    """
    Represents a test's output.
    
    Attributes
    ----------
    raised_exception : `None`, `BaseException`
        The raised exception by the test.
    returned_value : `None`, `Any`
        The returned value by the test.
    """
    __slots__ = ('raised_exception', 'returned_value')
    
    def __new__(cls, returned_value, raised_exception):
        """
        Creates a new result state.
        
        Parameters
        ----------
        returned_value : `None`, `Any`
            The returned value by the test.
        raised_exception : `None`, `BaseException`
            The raised exception by the test.
        """
        self = object.__new__(cls)
        self.raised_exception = raised_exception
        self.returned_value = returned_value
        return self
    
    
    def __repr__(self):
        """Returns the representation of the result state."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        returned_value = self.returned_value
        if (returned_value is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' returned_value')
            repr_parts.append(repr(returned_value))
        
        raised_exception = self.raised_exception
        if (raised_exception is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' raised_exception')
            repr_parts.append(repr(raised_exception))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two result states are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.raised_exception != other.raised_exception:
            return False
        
        if self.returned_value != other.returned_value:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the result state's hash value."""
        hash_value = 0
        
        raised_exception = self.raised_exception
        if (raised_exception is not None):
            hash_value ^= 1 << 4
            hash_value ^= hash_object(raised_exception)
        
        returned_value = self.returned_value
        if (returned_value is not None):
            hash_value ^= 1 << 8
            hash_value ^= hash_object(returned_value)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the result state.
        
        Returns
        -------
        new : ``ResultState``
        """
        new = object.__new__(type(self))
        new.raised_exception = self.raised_exception
        new.returned_value = self.returned_value
        return new
    
    
    def __bool__(self):
        """Returns whether the result state holds anythings."""
        if (self.raised_exception is not None):
            return True
        
        if (self.returned_value is not None):
            return True
        
        return False
    
    
    def with_return(self, returned_value):
        """
        Creates a new call state overwriting the old one.
        
        Parameters
        ----------
        returned_value : `None`, `Any`
            The returned value by the test.
        
        Returns
        -------
        new : ``ResultState``
        """
        new = object.__new__(type(self))
        new.raised_exception = None
        new.returned_value = returned_value
        return new
    
    
    def with_exception(self, raised_exception):
        """
        Creates a new call state overwriting the old one.
        
        Parameters
        ----------
        raised_exception : `None`, `BaseException`
            The raised exception by the test.
        
        Returns
        -------
        new : ``ResultState``
        """
        new = object.__new__(type(self))
        new.raised_exception = raised_exception
        new.returned_value = None
        return new


class Handle(RichAttributeErrorBaseType):
    """
    Handles a test.
    
    Attributes
    ----------
    case : ``TestCase``
        The parent test case.
    environments : `None`, `tuple` of ``Environment``
        Environments to use to use when testing.
    final_call_state : `None`, ``CallState``
        The final call state, with which the test is called.
    final_result_state : `None`, ``ResultState``
        Final result state after wrappers processed the original.
    original_call_state : `None`, ``CallState``
        Vanilla call state.
    original_result_state : `None`, ``ResultState``
        Result state created from the test's result.
    test : `callable`
        The test to invoke.
    wrappers : `None`, `tuple` of ``WrapperBase``
        Wrappers wrapping the test.
    """
    __slots__ = (
        'case', 'environments', 'final_call_state', 'final_result_state', 'original_call_state',
        'original_result_state', 'test', 'wrappers'
    )
    
    def __new__(cls, case, test, wrappers, environments):
        """
        Creates a new test handle.
        
        Parameters
        ----------
        case : ``TestCase``
            The parent test case.
        test : `callable`
            The test to call.
        wrappers : `None`, `tuple` of ``WrapperBase``
            Wrappers wrapping the test.
        environments : `None`, `tuple` of ``Environment``
            Environments to use to use when testing.
        """
        self = object.__new__(cls)
        
        self.case = case
        self.test = test
        self.wrappers = wrappers
        self.environments = environments
        
        self.original_call_state = None
        self.final_call_state = None
        
        self.original_result_state = None
        self.final_result_state = None
        
        return self
    
    
    def __repr__(self):
        """Returns the test handle's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' test=')
        repr_parts.append(reprlib.repr(self.test))
        
        wrappers = self.wrappers
        if (wrappers is not None):
            repr_parts.append(', wrappers=')
            repr_parts.append(repr(wrappers))
        
        original_call_state = self.original_call_state
        if (original_call_state is not None) and original_call_state:
            repr_parts.append(', original_call_state=')
            repr_parts.append(repr(original_call_state))
        
        final_call_state = self.final_call_state
        if (final_call_state is not None) and final_call_state:
            repr_parts.append(', final_call_state=')
            repr_parts.append(repr(final_call_state))
            
        original_result_state = self.original_result_state
        if (original_result_state is not None) and original_result_state:
            repr_parts.append(', original_result_state=')
            repr_parts.append(repr(original_result_state))
        
        final_result_state = self.final_result_state
        if (final_result_state is not None) and final_result_state:
            repr_parts.append(', final_result_state=')
            repr_parts.append(repr(final_result_state))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _initialise_test_wrapper_contexts(self, test_wrapper_contexts):
        """
        Initialises the wrappers of the test handle.
        
        Parameters
        ----------
        test_wrapper_contexts : `list` of `GeneratorType`
            Test wrappers to initialize into
        """
        wrappers = self.wrappers
        if wrappers is not None:
            for wrapper in wrappers:
                context = wrapper.context(self)
                test_wrapper_contexts.append(context)
    
    
    def _start_test_wrapper_contexts(self, test_wrapper_contexts):
        """
        Starts the text wrapper contexts.
        
        Parameters
        ----------
        test_wrapper_contexts : `list` of `GeneratorType`
            Test wrappers to initialize into
        
        Returns
        -------
        test_result : `None`, ``Result``
            Result of the test.
        """
        for test_wrapper_context in test_wrapper_contexts:
            try:
                test_result = test_wrapper_context.send(None)
            except StopIteration as err:
                test_result = err.value
            
            if (test_result is not None):
                return test_result
    
    
    def _enter_test_wrapper_contexts(self, test_wrapper_contexts):
        """
        Enters the text wrapper contexts passing them a ``CallState``, expecting them to return a new call state, or
        a test result.
        
        Parameters
        ----------
        test_wrapper_contexts : `list` of `GeneratorType`
            Test wrappers to start.
        
        Returns
        -------
        test_result : `None`, ``Result``
            Result of the test.
        """
        call_state = CallState()
        self.original_call_state = call_state
        
        try:
            for test_wrapper_context in test_wrapper_contexts:
                try:
                    enter_result = test_wrapper_context.send(call_state)
                except StopIteration as err:
                    enter_result = err.value
                
                if enter_result is None:
                    continue
                
                if isinstance(enter_result, CallState):
                    call_state = enter_result
                
                if isinstance(enter_result, Result):
                    return enter_result
            
        finally:
            self.final_call_state = call_state
    
    
    def _get_call_parameters(self):
        """
        Gets call parameters to invoke the test with.
        
        Returns
        -------
        positional_parameters : `list` of `Any`
            Positional parameters to call the test with.
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to call the test with.
        """
        call_state = self.final_call_state
        
        if call_state is None:
            positional_parameters = None
            keyword_parameters = None
        
        else:
            positional_parameters = call_state.positional_parameters
            keyword_parameters = call_state.keyword_parameters
        
        if (positional_parameters is None):
            positional_parameters = []
        
        if (keyword_parameters is None):
            keyword_parameters = {}
        
        return positional_parameters, keyword_parameters
    
    
    def _invoke_test(self, environment_manager):
        """
        Invokes the test of the test handle.
        
        Parameters
        ----------
        environment_manager : ``EnvironmentManager``
            Testing environment manager.
        """
        positional_parameters, keyword_parameters = self._get_call_parameters()
        
        test = self.test
        
        environment = environment_manager.get_environment_for_test(test)
        
        result_state = environment.run(test, positional_parameters, keyword_parameters)
        
        gc.collect()
        gc.collect()
        
        self.original_result_state = result_state
    
    
    def _exit_test_wrapper_contexts(self, test_wrapper_contexts):
        """
        Exits the text wrapper contexts passing them a ``ResultState``, expecting them to return a new call state, or
        a test result.
        
        Parameters
        ----------
        test_wrapper_contexts : `list` of `GeneratorType`
            Test wrappers to start.
        
        Returns
        -------
        test_result : `None`, ``Result``
            Result of the test.
        """
        result_state = self.original_result_state
        
        try:
            for test_wrapper_context in test_wrapper_contexts:
                try:
                    exit_result = test_wrapper_context.send(result_state)
                except StopIteration as err:
                    exit_result = err.value
                
                if exit_result is None:
                    continue
                
                if isinstance(exit_result, ResultState):
                    result_state = exit_result
                
                if isinstance(exit_result, Result):
                    return exit_result
            
        finally:
            self.final_result_state = result_state
    
    
    def _build_default_test_result(self):
        """
        Builds test result if non of the wrappers did before.
        
        Returns
        -------
        test_result : ``Result``
            Result of the test.
        """
        test_result = Result(self)
        
        raised_exception = self.final_result_state.raised_exception
        if (raised_exception is not None):
            if isinstance(raised_exception, AssertionException):
                test_result = test_result.with_assertion(raised_exception)
            
            else:
                test_result = test_result.with_exception(None, raised_exception, False)
        
        return test_result
    
    
    def _iter_applied_environments(self):
        """
        Iterates over the applies the environment wrappers to the test.
        
        This method is an iterable generator.
        
        Yields
        ------
        environment : ``Environment``
        """
        environments = self.environments
        if (environments is not None):
            yield from environments
    
    def invoke(self, environment_manager):
        """
        Invokes the test.
        
        Parameters
        ----------
        environment_manager : ``EnvironmentManager``
            Testing environment manager.
        
        Returns
        -------
        test_result : ``Result``
            Result of the test.
        """
        environment_manager = environment_manager.with_environment(*self._iter_applied_environments())
        
        test_wrapper_contexts = []
        try:
            self._initialise_test_wrapper_contexts(test_wrapper_contexts)
            
            test_result = self._start_test_wrapper_contexts(test_wrapper_contexts)
            if (test_result is not None):
                return test_result
            
            
            test_result = self._enter_test_wrapper_contexts(test_wrapper_contexts)
            if (test_result is not None):
                return test_result
            
            try:
                self._invoke_test(environment_manager)
            except:
                self._exit_test_wrapper_contexts(test_wrapper_contexts)
                raise
            
            else:
                test_result = self._exit_test_wrapper_contexts(test_wrapper_contexts)
                if (test_result is not None):
                    return test_result
            
            return self._build_default_test_result()
            
        finally:
            for test_wrapper_context in test_wrapper_contexts:
                test_wrapper_context.close()
    
    
    def get_test_documentation(self):
        """
        Returns the test's documentation.
        
        Returns
        -------
        documentation : `None`, `str`
        """
        test_name = getattr(self.test, '__name__', None)
        if (test_name is None) or (not isinstance(test_name, str)):
            return None
        
        if self.case.name != test_name:
            return None
        
        raw_documentation = getattr(self.test, '__doc__', None)
        if (raw_documentation is None) or (not isinstance(raw_documentation, str)):
            return None
        
        lines = raw_documentation.split('\n')
        if not lines:
            return None
        
        for index in range(len(lines)):
            lines[index] = lines[index].rstrip()
        
        indentation_to_remove = 0
        
        while True:
            for line in lines:
                if len(line) <= indentation_to_remove:
                    continue
                
                if line[indentation_to_remove] in (' ', '\t'):
                    continue
                
                break
            
            else:
                indentation_to_remove += 1
                continue
            
            break
        
        
        for index in range(len(lines)):
            lines[index] = lines[index][indentation_to_remove:]
        
        while True:
            if lines[-1]:
                break
            
            del lines[-1]
            if not lines:
                return None
        
        while True:
            if lines[0]:
                break
            
            del lines[0]
            continue
        
        
        documentation_parts = []
        index = 0
        line_count = len(lines)
        
        while True:
            documentation_parts.append('> ')
            documentation_parts.append(lines[index])
            
            index += 1
            if index == line_count:
                break
            
            documentation_parts.append('\n')
            continue
        
        return ''.join(documentation_parts)
