__all__ = ('TestRunner', 'run_tests_in')

import sys
from functools import partial as partial_func
from os import getcwd as get_current_working_directory
from os.path import sep as PATH_SEPARATOR

from scarletio import DEFAULT_ANSI_HIGHLIGHTER, RichAttributeErrorBaseType, include, render_exception_into

from ... import __package__ as PACKAGE_NAME
from ...return_codes import (
    RETURN_CODE_FAILURE, RETURN_CODE_SUCCESS, RETURN_CODE_TEST_RUNNER_STOPPED, RETURN_CODE_UNSET
)

from ..environment import EnvironmentManager
from ..events import (
    FileLoadDoneEvent, FileRegistrationEvent, FileRegistrationDoneEvent, FileTestingDoneEvent, SourceLoadFailureEvent,
    TestDoneEvent, TestingEndEvent, TestingStartEvent
)
from ..file import FileSystemEntry, iter_collect_test_files_in

from .context import RunnerContext


create_default_event_handler_manager = include('create_default_event_handler_manager')


def setup_test_library_import():
    """
    Setups test directory import if not on path instead running it relatively.
    """
    split = PACKAGE_NAME.split('.')
    if len(split) <= 1:
        return None
    
    module = __import__(PACKAGE_NAME)
    
    for directory_name in split[1:]:
        module = module.__dict__[directory_name]
    
    sys.modules[split[-1]] = module


def _add_to_system_path_callback(path, runner):
    """
    Removes the given path from `sys.path`.
    
    Parameters
    ----------
    path : `str`
        The path to remove.
    runner : ``TestRunner``
        The respective test runner.
    """
    if path not in sys.path:
        sys.path.append(path)
        
    

def _remove_from_system_path_callback(path, runner):
    """
    Removes the given path from `sys.path`.
    
    Parameters
    ----------
    path : `str`
        The path to remove.
    runner : ``TestRunner``
        The respective test runner.
    """
    try:
        sys.path.remove(path)
    except ValueError:
        pass


def _ignore_test_call_frame(frame):
    """
    Ignores test runner frames when rendering event handler exception
    
    Parameters
    ----------
    frame : ``FrameProxyBase``
        The frame to check.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    file_name = frame.file_name
    name = frame.name
    line = frame.line
    
    if file_name == __file__:
        if name == 'run':
            if line == 'event_handler(event)':
                should_show_frame = False
    
    return should_show_frame


def _render_event_exception(event_handler, event, exception):
    """
    Renders exception occurred inside of en event handler.
    
    Parameters
    ----------
    event_handler : `callable`
        The event handler which failed to run.
    
    event : ``EventBase``
        The dispatched event.
    
    exception : `BaseException`
        The occurred exception.
    """
    
    exception_message_parts = [
        'Exception occurred meanwhile running event handler: ',
        repr(event_handler),
        ' with event ',
        repr(event),
        '\n\n'
    ]
    
    exception_message_parts = render_exception_into(
        exception,
        exception_message_parts,
        filter = _ignore_test_call_frame,
        highlighter = DEFAULT_ANSI_HIGHLIGHTER,
    )
    
    return ''.join(exception_message_parts)


class TestRunner(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    _path_parts : `None | list<str>`
        Added path parts to specify from which which directory we want to collect the tests from.
    _return_code : `int`
        The return code of the test runner.
    _source_directory : `str`
        The path to run tests from.
    _sources : `set<str>`
        Sources to import before executing any test.
    _stopped : `bool`
        Whether testing is stopped.
    _teardown_callbacks : `None`, `list` of `callable`
        Functions to call when the tests are finished.
    environment_manager : ``EnvironmentManager``
        Testing environment manager.
    event_handler_manager : ``EventHandlerManager``
        Event handler container.
    
    Utility Methods
    ---------------
    - ``.run``
    - ``.stop``
    - ``.add_teardown_callback``
    - ``.get_return_code``
    - ``.set_return_code``
    """
    __slots__ = (
        '_path_parts', '_return_code', '_source_directory', '_sources', '_stopped', '_teardown_callbacks',
        'environment_manager', 'event_handler_manager'
    )
    
    def __new__(
        cls, source_directory, sources, path_parts = None, *, environment_manager = None, event_handler_manager = None
    ):
        """
        Creates a new test runner instance.
        
        Parameters
        ----------
        source_directory : `str`
            The path to run tests from.
        sources : `set<str>`
            Sources to import before executing any test.
        path_parts : `None | list<str>` = `None`, Optional
            Added path parts to specify from which which directory we want to collect the tests from.
        environment_manager : `None`, ``EnvironmentManager`` = `None`, Optional (Keyword only)
            Testing environment manager.
        event_handler_manager : `None`, ``EventHandlerManager`` = `None`, Optional (Keyword only)
            Event handler container.
        """
        if (path_parts is not None):
            if path_parts:
                path_parts = path_parts.copy()
            else:
                path_parts = None
            
        if environment_manager is None:
            environment_manager = EnvironmentManager()
        
        environment_manager = environment_manager.populate()
        
        if event_handler_manager is None:
            event_handler_manager = create_default_event_handler_manager()
        
        self = object.__new__(cls)
        self._path_parts = path_parts
        self._return_code = RETURN_CODE_UNSET
        self._source_directory = source_directory
        self._sources = sources
        self._stopped = False
        self._teardown_callbacks = None
        self.environment_manager = environment_manager
        self.event_handler_manager = event_handler_manager
        return self
    
    
    def _setup(self):
        """
        Setups the test dependencies.
        """
        # Add source directory to sys.path if not there
        source_directory = self._source_directory
        
        if source_directory in sys.path:
            source_directory_in_system_paths = True
        else:
            sys.path.append(source_directory)
            source_directory_in_system_paths = False
        
        if not source_directory_in_system_paths:
            self.add_teardown_callback(partial_func(_remove_from_system_path_callback, source_directory))
        
        # Remove working directory from sys.path if under source directory
        working_directory = get_current_working_directory()
        if (
            working_directory in sys.path and
            len(working_directory) > len(source_directory) and
            working_directory.startswith(source_directory) and
            working_directory[len(source_directory)] == PATH_SEPARATOR
        ):
            working_directory_under_source = True
            try:
                sys.path.remove(working_directory)
            except ValueError:
                pass
        else:
            working_directory_under_source = False
        
        if not working_directory_under_source:
            self.add_teardown_callback(partial_func(_add_to_system_path_callback, working_directory))
        
        setup_test_library_import()
    
    
    def add_teardown_callback(self, callback):
        """
        Adds a callback to run when the tests are finished.
        
        Parameters
        ----------
        callback : `callable`
            The callback to add.
        """
        teardown_callbacks = self._teardown_callbacks
        if (teardown_callbacks is None):
            teardown_callbacks = []
            self._teardown_callbacks = teardown_callbacks
        
        teardown_callbacks.append(callback)
    
    
    def _exhaust_teardown_callbacks(self):
        """
        Runs the teardown callbacks.
        """
        teardown_callbacks = self._teardown_callbacks
        self._teardown_callbacks = None
        
        if (teardown_callbacks is not None):
            while teardown_callbacks:
                teardown_callbacks.pop()(self)
    
    
    def _teardown(self):
        """
        Clears up after the tests ran.
        """
        self._exhaust_teardown_callbacks()
    
    
    def _run_generator(self):
        """
        Runs the tests of the runner. Witch each iteration step it drops back the created event.
        
        This method is an iterable generator.
        
        Yields
        ------
        event : ``EventBase``
        """
        context = None
        
        try:
            # Setup
            self._setup()
            
            # Build context.
            path_parts = self._path_parts
            if path_parts is None:
                file_system_entries = [
                    FileSystemEntry(self._source_directory, source, None) for source in self._sources
                ]
            else:
                file_system_entries = [FileSystemEntry(self._source_directory, path_parts[0], path_parts[1:])]
            
            context = RunnerContext(self, file_system_entries)
            
            # Import plugins.
            for source in self._sources:
                try:
                    __import__(source)
                except BaseException as err:
                    yield SourceLoadFailureEvent(context, source, err)
                    return
            
            yield TestingStartEvent(context)
            
            # Collect test files
            for file_system_entry in context.file_system_entries:
                for test_file in iter_collect_test_files_in(file_system_entry):
                    context.register_file(test_file)
                    yield FileRegistrationEvent(context, test_file)
            
            yield FileRegistrationDoneEvent(context)
            
            # Load test files
            for registered_file in context.iter_registered_files_shallow():
                for test_file in registered_file.iter_test_files():
                    if test_file.is_directory():
                        test_file.get_module()
                        
                        yield FileLoadDoneEvent(context, test_file)
                        
                        if test_file.is_loaded_with_failure():
                            break
                        
                        yield FileTestingDoneEvent(context, test_file)
                    
                    else:
                        test_file.try_load_test_cases()
                        
                        yield FileLoadDoneEvent(context, test_file)
                        
                        # Run test file if loaded successfully
                        if test_file.is_loaded_with_success():
                            
                            for result in test_file.iter_invoke_test_cases(self.environment_manager):
                                yield TestDoneEvent(context, result)
                            
                            yield FileTestingDoneEvent(context, test_file)
            
            yield TestingEndEvent(context)
        
        except GeneratorExit:
            self.set_return_code(RETURN_CODE_TEST_RUNNER_STOPPED)
            raise
        
        else:
            if (context is not None):
                self.set_return_code(RETURN_CODE_FAILURE if context.has_any_failure() else RETURN_CODE_SUCCESS)
        
        finally:
            self._teardown()
    
    
    def run(self):
        """
        Runs the tests of the test runner.
        
        Returns
        -------
        return_code : `int`
        """
        if self._stopped:
            return self.get_return_code()
        
        event_handler_manager = self.event_handler_manager
        
        for event in self._run_generator():
            for event_handler in event_handler_manager.iter_handlers_for_event(event):
                try:
                    event_handler(event)
                except (KeyboardInterrupt, SystemExit):
                    raise
                
                except BaseException as err:
                    sys.stderr.write(_render_event_exception(event_handler, event, err))
            
            if self._stopped:
                break
        
        return self.get_return_code()
    
    
    def stop(self):
        """
        Stops the testing step loop.
        """
        self._stopped = True
        self.set_return_code(RETURN_CODE_TEST_RUNNER_STOPPED)
    
    
    def get_return_code(self):
        """
        Gets the set return code.
        
        Returns
        -------
        return_code : `int`
        """
        return_code = self._return_code
        if return_code == RETURN_CODE_UNSET:
            return_code = RETURN_CODE_SUCCESS
        
        return return_code
    
    
    def set_return_code(self, return_code):
        """
        Sets the test runner's return code if not set yet.
        
        Parameters
        ----------
        return_code : `int`
            Return code to set.
        """
        if self._return_code == RETURN_CODE_UNSET:
            self._return_code = return_code


def run_tests_in(source_directory, sources, test_collection_route):
    """
    Runs tests from the given `source_directory` and collects them from the given `test_collection_route`.
    Or from `sources` if not specified.
    
    Parameters
    ----------
    source_directory : `str`
        The path to import the sources from.
    sources : `set<str>`
        Sources to import before executing any test.
    test_collection_route : `None | list<str>`
        Added path parts to specify from which which directory we want to collect the tests from.
    
    Returns
    -------
    return_code : `int`
    """
    return TestRunner(source_directory, sources, test_collection_route).run()
