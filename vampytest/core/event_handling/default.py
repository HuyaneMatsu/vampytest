__all__ = ('create_default_event_handler_manager',)

from ..events import FileLoadDoneEvent, FileRegistrationDoneEvent, FileTestingDoneEvent, TestDoneEvent, TestingEndEvent

from .base import EventHandlerManager
from .default_output_writer import OutputWriter
from .text_styling import style_text, TextForeground

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
    event_handler_manager.events(output_formatter.file_testing_done)
    event_handler_manager.events(output_formatter.testing_end)
    
    return event_handler_manager


class DefaultEventFormatter(RichAttributeErrorBaseType):
    """
    Default output formatter for test runner.
    
    Attributes
    ----------
    rendered_entries : `set` of ``FileSystemEntry``
        The rendered entries by the
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    """
    __slots__ = ('rendered_entries', 'output_writer',)
    
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
        self.rendered_entries = set()
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
            message_parts = self._maybe_render_test_file_into(
                [],
                file.entry,
                name = style_text(
                    file.entry.get_name(),
                    foreground = TextForeground.red,
                ),
            )
            
            self.output_writer.write_line(''.join(message_parts))
    
    
    def _maybe_render_test_file_into(self, into, entry, *, name=None):
        """
        Helpers method for rendering file structure tree.
        
        Parameters
        ----------
        into : `list` of `str`
            List to render the structure parts into.
        entry : ``FileSystemEntry``
            The entry to render.
        name : `None`, `str` = `None`, Optional (Keyword only)
            Custom name to use as the entry's name.
        
        Returns
        -------
        into : `list` of `str`
        """
        rendered_entries = self.rendered_entries
        
        if (entry not in rendered_entries):
            for sub_entry in entry.iter_parents():
                if sub_entry in rendered_entries:
                    continue
                    
                into = sub_entry.render_into(into)
                rendered_entries.add(sub_entry)
            
            into = entry.render_into(into, name=name)
            rendered_entries.add(entry)
        
        return into
    
    
    def test_done(self, event: TestDoneEvent):
        """
        Called when a test is done.
        
        Parameters
        ----------
        event : ``TestDoneEvent``
            The dispatched event.
        """
        test_file = event.result_group.case.get_test_file()
        if (test_file is None):
            # Should not happen
            return
        
        message_parts = self._maybe_render_test_file_into([], test_file.entry)
        
        result_group = event.result_group
        if result_group.is_skipped():
            keyword = 'S'
            foreground = TextForeground.light_blue
        
        elif result_group.is_passed():
            keyword = 'P'
            foreground = TextForeground.green
        
        elif result_group.is_failed():
            keyword = 'F'
            foreground = TextForeground.red
        
        else:
            keyword = '?'
            foreground = TextForeground.white
        
        message_parts = test_file.entry.render_custom_sub_directory_into(
            message_parts,
            style_text(
                f'{keyword} {result_group.case.name}',
                foreground = foreground,
            ),
            result_group.case.is_last(),
        )
        
        self.output_writer.write_line(''.join(message_parts))
    


    def file_testing_done(self, event: FileTestingDoneEvent):
        """
        Called when all tests of a file is done
        
        Parameters
        ----------
        event : ``FileTestingDoneEvent``
            The dispatched event.
        """
        message_parts = self._maybe_render_test_file_into([], event.file.entry)
        if message_parts:
            self.output_writer.write_line(''.join(message_parts))
    
    
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
        
        
        for result_group in context.iter_failed_result_groups():
            for failure_message in result_group.iter_failure_messages():
                output_writer.write_line(failure_message)
                output_writer.write_break_line()
        
        failed_count = context.get_failed_test_count()
        failed_message_part = f'{failed_count} failed'
        if failed_count:
            failed_message_part = style_text(failed_message_part, foreground = TextForeground.red)
        
        
        skipped_count = context.get_skipped_test_count()
        skipped_message_part = f'{skipped_count} skipped'
        if skipped_count:
            skipped_message_part = style_text(skipped_message_part, foreground = TextForeground.cyan)
        
        
        passed_count = context.get_passed_test_count()
        passed_message_part = f'{passed_count} passed'
        if passed_count:
            passed_message_part = style_text(passed_message_part, foreground = TextForeground.green)
        
        
        output_writer.write(f'{failed_message_part} | {skipped_message_part} | {passed_message_part}')
        if load_failures:
            output_writer.write(
                style_text(
                    f' | {len(load_failures)} files failed to load',
                    foreground = TextForeground.red,
                )
            )
        output_writer.end_line()
