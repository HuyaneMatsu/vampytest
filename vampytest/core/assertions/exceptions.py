__all__ = ('AssertionException', )

from scarletio import export, render_frames_into
from scarletio.utils.trace import _get_exception_frames

from ..environment.default import __file__ as VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH
from ..environment.scarletio_coroutine import __file__ as VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH

from .assertion_conditional_base import __file__ as VAMPYTEST_ASSERTION_CONDITION_BASE_FILE_PATH
from .assertion_instance import __file__ as VAMPYTEST_ASSERTION_INSTANCE_FILE_PATH
from .assertion_subtype import __file__ as VAMPYTEST_ASSERTION_SUBTYPE_FILE_PATH


def _ignore_assertion_frames(file_name, name, line_number, line):
    """
    Ignores the frame where assertions are done.
    
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
    
    if file_name == VAMPYTEST_ASSERTION_CONDITION_BASE_FILE_PATH:
        if name == '__new__':
            if line == 'return self.invoke()':
                should_show_frame = False
        
        elif name == 'invoke':
            if line == 'raise AssertionException(self)':
                should_show_frame = False
    
    elif file_name == VAMPYTEST_ASSERTION_INSTANCE_FILE_PATH:
        if name == '__new__':
            if line == 'return self.invoke()':
                should_show_frame = False

    elif file_name == VAMPYTEST_ASSERTION_SUBTYPE_FILE_PATH:
        if name == '__new__':
            if line == 'return AssertionConditionalBase2Value.__new__(cls, value, type_, reverse=reverse)':
                should_show_frame = False
    
    elif file_name == VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH:
        if name == 'run':
            if line == 'returned_value = test(*positional_parameters, **keyword_parameters)':
                should_show_frame = False
    
    elif file_name == VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH:
        if name == '_run_async':
            if line == 'returned_value = await test(*positional_parameters, **keyword_parameters)':
                should_show_frame = False
    
    
    return should_show_frame



@export
class AssertionException(BaseException):
    """
    Raised when an exception fails.
    
    Attributes
    ----------
    assertion : ``AssertionBase``
        The failed assertion.
    """
    def __init__(self, assertion):
        """
        Creates a new condition exception.
        
        Parameters
        ----------
        assertion : ``AssertionBase``
            The failed assertion.
        """
        self.assertion = assertion
        BaseException.__init__(self, assertion)
    
    
    def render_failure_message_parts_into(self, failure_message_parts):
        """
        Renders the exception into the given list.
        
        Parameters
        ----------
        failure_message_parts : `list` of `str`
            A list to put the rendered strings into.
        
        Returns
        -------
        failure_message_parts : `list` of `str`
        """
        frames = _get_exception_frames(self)
        failure_message_parts.append('\n')
        render_frames_into(frames, failure_message_parts, filter=_ignore_assertion_frames)
        failure_message_parts.append('\n')
        self.assertion.render_failure_message_parts_into(failure_message_parts)
        return failure_message_parts
