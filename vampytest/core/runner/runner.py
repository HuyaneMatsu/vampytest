__all__ = ('TestRunner', 'run_tests_in')

import sys
from functools import partial as partial_func
from os.path import isfile as is_file, split as split_paths
from sys import path as system_paths, modules as system_modules

from ... import __package__ as PACKAGE_NAME

from ..environment import EnvironmentManager
from ..events import (
    FileLoadDoneEvent, FileRegistrationEvent, FileRegistrationDoneEvent, FileTestingDoneEvent, TestDoneEvent,
    TestingEndEvent, TestingStartEvent
)
from ..event_handling import create_default_event_handler_manager
from ..file import iter_collect_test_files

from .context import RunnerContext

from scarletio import RichAttributeErrorBaseType, render_exception_into


def setup_test_library_import():
    """
    Setups test directory import if not on path instead running it relatively.
    
    Returns
    -------
    added_system_path : `None`, `str`
        Returns the added system path if any.
    """
    split = PACKAGE_NAME.split('.')
    if len(split) <= 1:
        return None
    
    module = __import__(PACKAGE_NAME)
    for directory_name in split[1:]:
        module = module.__dict__[directory_name]
    
    system_modules[split[-1]] = module


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
        system_paths.remove(path)
    except ValueError:
        pass


def _ignore_test_call_frame(file_name, name, line_number, line):
    """
    Ignores test runner frames when rendering event handler exception
    
    Parameters
    ----------
    file_name : `str`
        The frame's respective file's name.
    name : `str`
        The frame's respective function's name.
    line_number : `int`
        The line's index where the exception occurred.
    line : `str`
        The frame's respective stripped line.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    if file_name == __file__:
        if name == 'run':
            if line == 'event_handler(event)':
                should_show_frame = False
    
    return should_show_frame


def _render_event_exception(event_handler, event, err):
    """
    Renders exception occurred inside of en event handler.
    
    Parameters
    ----------
    event_handler : `callable`
        The event handler which failed to run.
    
    event : ``EventBase``
        The dispatched event.
    
    err : `BaseException`
        The occurred exception.
    """
    
    exception_message_parts = [
        'Exception occurred meanwhile running event handler: ',
        repr(event_handler),
        ' with event ',
        repr(event),
        '\n\n'
    ]
    
    render_exception_into(err, exception_message_parts, filter=_ignore_test_call_frame)
    
    return ''.join(exception_message_parts)


class TestRunner(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    _base_path : `str`
        The path to run tests from.
    _path_parts : `list` of `str`   
        Added path parts to specify from which which directory we want to collect the tests from.
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
    """
    __slots__ = (
        '_base_path', '_path_parts', '_stopped', '_teardown_callbacks', 'environment_manager', 'event_handler_manager'
    )
    
    def __new__(cls, base_path, path_parts=None, *, environment_manager=None, event_handler_manager=None):
        """
        Parameters
        ----------
        base_path : `str`
            The path to run tests from.
        path_parts : `None`, `list` of `str` = `None`, Optional
            Added path parts to specify from which which directory we want to collect the tests from.
        environment_manager : `None`, ``EnvironmentManager`` = `None`, Optional (Keyword only)
            Testing environment manager.
        event_handler_manager : `None`, ``EventHandlerManager`` = `None`, Optional (Keyword only)
            Event handler container.
        """
        if path_parts is None:
            path_parts = []
        else:
            path_parts = path_parts.copy()
        
        if environment_manager is None:
            environment_manager = EnvironmentManager()
        
        environment_manager = environment_manager.populate()
        
        if event_handler_manager is None:
            event_handler_manager = create_default_event_handler_manager()
        
        self = object.__new__(cls)
        self._base_path = base_path
        self._path_parts = path_parts
        self._stopped = False
        self._teardown_callbacks = None
        self.environment_manager = environment_manager
        self.event_handler_manager = event_handler_manager
        return self
    
    
    def _setup(self):
        """
        Setups the test dependencies.
        """
        base_path = self._base_path
        path_parts = self._path_parts
        
        if is_file(base_path):
            base_path, file_name = split_paths(base_path)
            path_parts.insert(0, file_name)
        
        if base_path in system_paths:
            base_path_in_system_paths = True
        else:
            system_paths.append(base_path)
            base_path_in_system_paths = False
        
        self._base_path = base_path
        self._path_parts = path_parts
        
        if base_path_in_system_paths:
            self.add_teardown_callback(partial_func(_remove_from_system_path_callback, base_path))
        
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

        try:
            # Setup
            self._setup()
            
            context = RunnerContext(self)
            
            yield TestingStartEvent(context)
            
            # Collect test files
            for test_file in iter_collect_test_files(self._base_path, self._path_parts):
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
                    else:
                        test_file.try_load_test_cases()
                        
                        yield FileLoadDoneEvent(context, test_file)
                        
                        # Run test file if loaded successfully
                        if test_file.is_loaded_with_success():
                            
                            for result_group in test_file.iter_invoke_test_cases(self.environment_manager):
                                yield TestDoneEvent(context, result_group)
                            
                            yield FileTestingDoneEvent(context, test_file)
            
            yield TestingEndEvent(context)
        
        finally:
            self._teardown()
    
    
    def run(self):
        """
        Runs the tests of the test runner.
        """
        if self._stopped:
            return
        
        event_handler_manager = self.event_handler_manager
        
        for event in self._run_generator():
            for event_handler in event_handler_manager.iter_handlers_for_event(event):
                try:
                    event_handler(event)
                except BaseException as err:
                    sys.stderr.write(_render_event_exception(event_handler, event, err))
            
            if self._stopped:
                break
    
    
    def stop(self):
        """
        Stops the testing step loop.
        """
        self._stopped = True


def run_tests_in(base_path, path_parts):
    """
    Runs tests from the given `base_path` and collects them the added `path_parts`.
    
    Parameters
    ----------
    base_path : `str`
        The path to run tests from.
    path_parts : `list` of `str`
        Added path parts to specify from which which directory we want to collect the tests from.
    """
    TestRunner(base_path, path_parts).run()
