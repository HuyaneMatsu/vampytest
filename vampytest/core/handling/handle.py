__all__ = ('Handle',)

from reprlib import repr as short_repr

from scarletio import RichAttributeErrorBaseType, include

from ..contexts import ContextOutputCapturing

from .call_state import CallState
from .parameter_checking import check_parameter_mismatch


Result = include('Result')
AssertionException = include('AssertionException')


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
    test : ``FunctionType``
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
        test : `FunctionType`
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
        
        repr_parts.append(' test = ')
        repr_parts.append(short_repr(self.test))
        
        wrappers = self.wrappers
        if (wrappers is not None):
            repr_parts.append(', wrappers = ')
            repr_parts.append(repr(wrappers))
        
        original_call_state = self.original_call_state
        if (original_call_state is not None) and original_call_state:
            repr_parts.append(', original_call_state = ')
            repr_parts.append(repr(original_call_state))
        
        final_call_state = self.final_call_state
        if (final_call_state is not None) and final_call_state:
            repr_parts.append(', final_call_state = ')
            repr_parts.append(repr(final_call_state))
            
        original_result_state = self.original_result_state
        if (original_result_state is not None) and original_result_state:
            repr_parts.append(', original_result_state = ')
            repr_parts.append(repr(original_result_state))
        
        final_result_state = self.final_result_state
        if (final_result_state is not None) and final_result_state:
            repr_parts.append(', final_result_state = ')
            repr_parts.append(repr(final_result_state))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _collect_contexts_into(self, contexts):
        """
        Initialises the wrappers of the test handle.
        
        Parameters
        ----------
        contexts : `list` of ``ContextBase```
            Test contexts to put the new ones into.
        """
        wrappers = self.wrappers
        if wrappers is not None:
            for wrapper in wrappers:
                context = wrapper.get_context(self)
                if (context is not None):
                    contexts.append(context)
    
    
    def _start_contexts(self, contexts):
        """
        Starts the text wrapper contexts.
        
        Parameters
        ----------
        contexts : `list` of ``ContextBase``
            Contexts to start.
        
        Returns
        -------
        test_result : `None`, ``Result``
            Result of the test.
        """
        for context in contexts:
            test_result = context.start()
            if (test_result is not None):
                return test_result
    
    
    def _enter_contexts(self, contexts):
        """
        Enters the text wrapper contexts passing them a ``CallState``, expecting them to return a new call state, or
        a test result.
        
        Parameters
        ----------
        contexts : `list` of ``ContextBase``
            Contexts to enter.
        
        Returns
        -------
        test_result : `None`, ``Result``
            Result of the test.
        """
        call_state = CallState()
        self.original_call_state = call_state
        
        try:
            for context in contexts:
                test_result, new_call_state = context.enter(call_state)
                
                if (new_call_state is not None):
                    call_state = new_call_state
                
                if (test_result is not None):
                    return test_result
        
        finally:
            self.final_call_state = call_state
    
    
    def _exit_contexts(self, contexts):
        """
        Exits the contexts passing them a ``ResultState``, expecting them to return a result state, or a result.
        
        Parameters
        ----------
        contexts : `list` of ``ContextBase``
            Contexts to exit.
        
        Returns
        -------
        test_result : `None`, ``Result``
            Result of the test.
        """
        result_state = self.original_result_state
        
        try:
            for context in reversed(contexts):
                test_result, new_result_state = context.exit(result_state)
                
                if (new_result_state is not None):
                    result_state = new_result_state
                
                if (test_result is not None):
                    return test_result
            
        finally:
            self.final_result_state = result_state
    
    
    def _close_contexts(self, contexts, result):
        """
        Exits the contexts.
        
        Parameters
        ----------
        contexts : `list` of ``ContextBase``
            Contexts to exit.
        result : `None`, ``Result˙`
            Result of the test.
        """
        for context in reversed(contexts):
            context.close(result)
    
    
    def _get_call_parameters_nullable(self):
        """
        Gets the call parameters to invoke the test with. The output elements are nullable.
        
        Returns
        -------
        positional_parameters : `None | list<object>`
            Positional parameters to call the test with.
        keyword_parameters : `None | dict<str, object>`
            Keyword parameters to call the test with.
        """
        call_state = self.final_call_state
        
        if call_state is None:
            positional_parameters = None
            keyword_parameters = None
        
        else:
            positional_parameters = call_state.positional_parameters
            keyword_parameters = call_state.keyword_parameters
        
        return positional_parameters, keyword_parameters
    
    
    def _get_call_parameters(self):
        """
        Gets call parameters to invoke the test with.
        
        Returns
        -------
        positional_parameters : `list` of `object`
            Positional parameters to call the test with.
        keyword_parameters : `dict` of (`str`, `object`) items
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
    
    
    def _check_call_parameter_match(self):
        """
        Checks whether the call parameters match with the test's.
        
        Returns
        -------
        test_result : `None`, ``Result``
            Result of the test.
        """
        parameter_mismatch = check_parameter_mismatch(self.test, *self._get_call_parameters_nullable())
        if (parameter_mismatch is not None):
            return Result(self.case).with_handle(self).with_parameter_mismatch(parameter_mismatch)
    
    
    def _invoke_test(self, environment_manager):
        """
        Invokes the test of the test handle.
        
        Parameters
        ----------
        environment_manager : ``EnvironmentManager``
            Testing environment manager.
        """
        environment = environment_manager.get_environment_for_test(self.test)
        self.original_result_state = environment.run(self.test, *self._get_call_parameters())
    
    
    def _build_default_test_result(self):
        """
        Builds test result if non of the wrappers did before.
        
        Returns
        -------
        test_result : ``Result``
            Result of the test.
        """
        test_result = Result(self.case).with_handle(self)
        
        result_state = self.final_result_state
        if (result_state is not None) and result_state.is_raise():
            raised_exception = result_state.result
            if isinstance(raised_exception, AssertionException):
                test_result = test_result.with_assertion(raised_exception)
            else:
                test_result = test_result.with_exception(None, False, raised_exception)
        
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
        
        contexts = [ContextOutputCapturing()]
        test_result = None
        
        try:
            self._collect_contexts_into(contexts)
            
            test_result = self._start_contexts(contexts)
            if (test_result is not None):
                return test_result
            
            test_result = self._enter_contexts(contexts)
            if (test_result is not None):
                return test_result
            
            test_result = self._check_call_parameter_match()
            if (test_result is not None):
                return test_result
            
            self._invoke_test(environment_manager)
            
            test_result = self._exit_contexts(contexts)
            if (test_result is not None):
                return test_result
            
            test_result = self._build_default_test_result()
            return test_result
        
        finally:
            self._close_contexts(contexts, test_result)
    
    
    def get_test_documentation_lines(self):
        """
        Returns the test's documentation's lines if it has any.
        
        Returns
        -------
        documentation : `None | list<str>`
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
        
        return lines
