__all__ = ('ScarletioCoroutineEnvironment',)

from time import sleep as sync_sleep

from scarletio import copy_docs, EventThread

from ..handling import ResultState

from .constants import ENVIRONMENT_TYPE_COROUTINE
from .default import DefaultEnvironment


DEFAULT_TIMEOUT = 60.0


class ScarletioCoroutineEnvironment(DefaultEnvironment):
    """
    Implements a scarletio coroutine environment.
    
    Attributes
    ----------
    timeout : `None`, `int`
        The maximal timeout to interrupt tests before.
        
        Defaults to creating a new event loop every time if set as `None`.
    
    event_loop : `None`, ``EventThread``
        The event loop to use to run the test in.
    
    Class Attributes
    ----------------
    identifier : `int` = `ENVIRONMENT_TYPE_COROUTINE`
        Represents for which environment the test is applicable for.
    """
    __slots__ = ('event_loop', 'timeout',)
    
    identifier = ENVIRONMENT_TYPE_COROUTINE
    
    def __new__(cls, *, event_loop = None, timeout = DEFAULT_TIMEOUT):
        """
        Parameters
        ----------
        event_loop : `None`, ``EventThread`` = `None`, Optional (Keyword only)
            The event loop to use to run the test in.
            S
            Defaults to creating a new event loop every time if given as `None`.
            
        timeout : `None`, `str` = `DEFAULT_TIMEOUT`, Optional (Keyword only)
            The maximal timeout to interrupt tests before.
        """
        self = object.__new__(cls)
        self.event_loop = event_loop
        self.timeout = timeout
        return self
    
    
    @copy_docs(DefaultEnvironment.run)
    def run(self, test, positional_parameters, keyword_parameters):
        event_loop = self.event_loop
        create_event_loop = (event_loop is None)
        
        try:
            if create_event_loop:
                event_loop = EventThread(daemon = True, name = 'scarletio.run', start_later = False)
            
            try:
                return event_loop.run(
                    self._run_async(test, positional_parameters, keyword_parameters),
                    timeout = self.timeout,
                )
            except KeyboardInterrupt as exception:
                # In case it is frozen lets provide a better output. Better than nothing.
                raise KeyboardInterrupt(
                    f'`{type(self).__name__}.run` interrupted while running {test!r}.'
                ) from exception
        finally:
            if create_event_loop:
                if (event_loop is not None):
                    event_loop.stop()
                    event_loop = None
                    sync_sleep(0.0)
    
    
    async def _run_async(self, test, positional_parameters, keyword_parameters):
        """
        Runs the defined test with the given parameters.
        
        This method is a coroutine.
        
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
            returned_value = await test(*positional_parameters, **keyword_parameters)
        except BaseException as raised_exception:
            return ResultState().with_raise(raised_exception)
        
        return ResultState().with_return(returned_value)
    
    
    @copy_docs(DefaultEnvironment.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        event_loop = self.event_loop
        if (event_loop is not None):
            repr_parts.append(' event_loop = ')
            repr_parts.append(repr(event_loop))
            
            field_added = True
        
        else:
            field_added = False
        
        timeout = self.timeout
        if (timeout is None) or (timeout != DEFAULT_TIMEOUT):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' timeout = ')
            repr_parts.append(repr(timeout))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(DefaultEnvironment.shutdown)
    def shutdown(self):
        event_loop = self.event_loop
        if (event_loop is not None):
            event_loop.stop()
            sync_sleep(0.0)
