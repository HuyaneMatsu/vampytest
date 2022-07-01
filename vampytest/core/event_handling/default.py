__all__ = ('create_default_event_handler_manager',)

from ..events import FileLoadDoneEvent, FileRegistrationDoneEvent, TestDoneEvent, TestingEndEvent

from .base import EventHandlerManager
from .default_output_writer import OutputWriter

from scarletio import RichAttributeErrorBaseType


def create_default_event_handler_manager():
    """
    Creates a default event handler manager if non is given.
    
    Returns
    ----------
    event_handler_manager : ``EventHandlerManager``
    """
    event_handler_manager = EventHandlerManager()
    
    output_formatter = DefaultEventFormatter()
    event_handler_manager.events(output_formatter.file_registration_done)
    event_handler_manager.events(output_formatter.file_load_done)
    event_handler_manager.events(output_formatter.test_done)
    event_handler_manager.events(output_formatter.testing_end)
    
    return event_handler_manager


class DefaultEventFormatter(RichAttributeErrorBaseType):
    """
    Default output formatter for test runner.
    
    Attributes
    ----------
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    """
    __slots__ = ('output_writer',)
    
    def __new__(cls, output_writer=None):
        """
        Creates a new default event formatter.
        
        Parameters
        ----------
        output_writer : `None`, ``OutputWriter` = `None`, Optional
            The output writer to write the output with.
        """
        if (output_writer is None):
            output_writer = OutputWriter()
        
        self = object.__new__(cls)
        self.output_writer = output_writer
        return self
    
    
    def __repr__(self):
        """Returns the output formatter representation."""
        return f'<{self.__class__.__name__} output_writer={self.output_writer!r}>'
    
    
    def file_registration_done(self, event: FileRegistrationDoneEvent):
        """
        Called when all files are registered.
        
        Parameters
        ----------
        event : ``FileRegistrationDoneEvent``
            The dispatched event.
        """
        output_writer = self.output_writer
        output_writer.write_line(f'Collected {event.context.get_registered_file_count()} test file(s).')
        output_writer.write_break_line()
    
    
    def file_load_done(self, event: FileLoadDoneEvent):
        """
        Called when a test file is loaded.
        
        Parameters
        ----------
        event : ``FileLoadDoneEvent``
            The dispatched event.
        """
        file = event.file
        if file.is_loaded_with_failure():
            self.output_writer.write_line(f'! {file.import_route}')
    
    
    def test_done(self, event: TestDoneEvent):
        """
        Called when a test is done.
        
        Parameters
        ----------
        event : ``TestDoneEvent``
            The dispatched event.
        """
        result_group = event.result_group
        if result_group.is_skipped():
            keyword = 'S'
        
        elif result_group.is_passed():
            keyword = 'P'
        
        elif result_group.is_failed():
            keyword = 'F'
        
        else:
            keyword = '?'
        
        case = result_group.case
        
        self.output_writer.write_line(f'{keyword} {case.import_route}.{case.name}')
    
    
    def testing_end(self, event: TestingEndEvent):
        """
        Called when a test is done.
        
        Parameters
        ----------
        event : ``TestDoneEvent``
            The dispatched event.
        """
        output_writer = self.output_writer
        output_writer.write_break_line()
        
        context = event.context
        
        load_failures = context.get_file_load_failures()
        
        for load_failure in load_failures:
            message = ''.join([
                'Exception occurred while loading:\n',
                load_failure.path,
                '\n\n',
                load_failure.exception_message,
            ])
            
            output_writer.write_line(message)
            output_writer.write_break_line()
        
        failed_result_groups = context.get_failed_result_groups()
        for result_group in failed_result_groups:
            for failure_message in result_group.iter_failure_messages():
                output_writer.write_line(failure_message)
                output_writer.write_break_line()
        
        output_writer.write(
            f'{len(failed_result_groups)} failed | '
            f'{context.get_skipped_test_count()} skipped | '
            f'{context.get_passed_test_count()} passed'
        )
        if load_failures:
            output_writer.write(f' | {len(load_failures)} files failed to load')
        output_writer.end_line()
