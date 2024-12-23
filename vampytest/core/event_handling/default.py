__all__ = ('create_default_event_handler_manager',)

from sys import platform as PLATFORM

from scarletio import (
    DEFAULT_ANSI_HIGHLIGHTER, HIGHLIGHT_TOKEN_TYPES, RichAttributeErrorBaseType, add_highlighted_part_into, export
)

from ..events import (
    FileLoadDoneEvent, FileRegistrationDoneEvent, FileTestingDoneEvent, SourceLoadFailureEvent, TestDoneEvent,
    TestingEndEvent
)
from .base import EventHandlerManager
from .default_output_writer import OutputWriter
from .rendering_helpers.load_failure_rendering import render_load_failure_exception
from .rendering_helpers.result_modifier_parameters import build_result_modifier_parameters
from .rendering_helpers.writers import write_load_failure, write_result_failing, write_result_informal


IS_WINDOWS = PLATFORM == 'win32'


@export
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
    event_handler_manager.events(output_formatter.source_load_failure)
    
    return event_handler_manager


class DefaultEventFormatter(RichAttributeErrorBaseType):
    """
    Default output formatter for test runner.
    
    Attributes
    ----------
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    rendered_entries : `set<FileSystemEntry>`
        The  already rendered file system entries.
    
    output_writer : ``OutputWriter``
        The output writer to write the output with.
    """
    __slots__ = ('highlighter', 'rendered_entries', 'output_writer',)
    
    def __new__(cls, *, highlighter = ..., output_writer = ...):
        """
        Creates a new default event formatter.
        
        Parameters
        ----------
        highlighter : `None | HighlightFormatterContext`, Optional (Keyword only)
            Highlighter to use.
        
        output_writer : `OutputWriter`, Optional (Keyword only)
            The output writer to write the output with.
        """
        # highlighter
        if highlighter is ...:
            if IS_WINDOWS:
                highlighter = None
            else:
                highlighter = DEFAULT_ANSI_HIGHLIGHTER
        
        # output_writer
        if (output_writer is ...):
            output_writer = OutputWriter()
        
        self = object.__new__(cls)
        self.highlighter = highlighter
        self.rendered_entries = set()
        self.output_writer = output_writer
        return self
    
    
    def __repr__(self):
        """Returns the output formatter representation."""
        repr_parts = ['<', type(self).__name__]
        
        # highlighter
        highlighter = self.highlighter
        if (highlighter is not None):
            repr_parts.append(' highlighter = ')
            repr_parts.append(repr(highlighter))
            repr_parts.append(',')
        
        # output_writer
        repr_parts.append(' output_writer = ')
        repr_parts.append(repr(self.output_writer))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
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
                name = ''.join(
                    add_highlighted_part_into(
                        HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE, file.entry.get_name(), self.highlighter, []
                    )
                ),
            )
            
            self.output_writer.write_line(''.join(message_parts))
    
    
    def _maybe_render_test_file_into(self, into, entry, *, name = None):
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
            
            into = entry.render_into(into, name = name)
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
        test_file = event.result.case.get_test_file()
        if (test_file is None):
            # Should not happen
            return
        
        message_parts = self._maybe_render_test_file_into([], test_file.entry)
        
        result = event.result
        if result.is_skipped():
            keyword = 'S'
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEUTRAL
        
        elif result.is_conflicted():
            keyword = 'C'
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE
        
        elif result.is_informal():
            keyword = 'I'
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_POSITIVE
        
        elif result.is_passed():
            keyword = 'P'
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_POSITIVE
        
        elif result.is_failed():
            keyword = 'F'
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE
        
        else:
            keyword = '?'
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_UNKNOWN
        
        result_modifiers = build_result_modifier_parameters(result.get_modifier_parameters())
        message_parts = test_file.entry.render_custom_sub_directory_into(
            message_parts,
            ''.join(
                add_highlighted_part_into(
                    token_type, f'{keyword} {result.case.name}{result_modifiers}', self.highlighter, []
                )
            ),
            result.is_last() and result.case.is_last(),
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
            write_load_failure(output_writer, load_failure, self.highlighter)
        
        for result in context.iter_failed_results():
            write_result_failing(output_writer, result, self.highlighter)
        
        failed_count = context.get_failed_test_count()
        if not failed_count:
            for result in context.iter_informal_results():
                write_result_informal(output_writer, result, self.highlighter)
        
        # build the summary line
        message_parts = []
        highlighter = self.highlighter
        
        # Failed
        if failed_count:
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE
        else:
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT
        message_parts = add_highlighted_part_into(
            token_type, f'{failed_count} failed', highlighter, message_parts
        )
        
        # Separator
        message_parts = add_highlighted_part_into(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, message_parts
        )
        message_parts = add_highlighted_part_into(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT, '|', highlighter, message_parts
        )
        message_parts = add_highlighted_part_into(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, message_parts
        )
        
        # Skipped
        skipped_count = context.get_skipped_test_count()
        if skipped_count:
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEUTRAL
        else:
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT
        message_parts = add_highlighted_part_into(
            token_type, f'{skipped_count} skipped', highlighter, message_parts
        )
        
        # Separator
        message_parts = add_highlighted_part_into(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, message_parts
        )
        message_parts = add_highlighted_part_into(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT, '|', highlighter, message_parts
        )
        message_parts = add_highlighted_part_into(
            HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, message_parts
        )
        
        # passed
        passed_count = context.get_passed_test_count()
        if passed_count:
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_POSITIVE
        else:
            token_type = HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT
        message_parts = add_highlighted_part_into(
            token_type, f'{passed_count} passed', self.highlighter, message_parts
        )
        
        if load_failures:
            # Separator
            message_parts = add_highlighted_part_into(
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, message_parts
            )
            message_parts = add_highlighted_part_into(
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT, '|', highlighter, message_parts
            )
            message_parts = add_highlighted_part_into(
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, message_parts
            )
            
            # load_failures
            message_parts = add_highlighted_part_into(
                HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_TEXT_NEGATIVE,
                f'{len(load_failures)} files failed to load',
                highlighter,
                message_parts,
            )
        
        output_writer.write(''.join(message_parts))
        output_writer.end_line()
    
    
    def source_load_failure(self, event: SourceLoadFailureEvent):
        """
        Called when a source is failed to load.
        
        Parameters
        ----------
        event : ``TestDoneEvent``
            The dispatched event.
        """
        output_writer = self.output_writer
        output_writer.write_line(f'Failed to import {event.source} from {event.context.runner._source_directory}')
        output_writer.write_break_line()
        output_writer.write(render_load_failure_exception(event.exception, self.highlighter))
        output_writer.end_line()
