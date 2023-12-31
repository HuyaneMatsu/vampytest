__all__ = ('AssertionException', )

from scarletio import export, render_frames_into
from scarletio.utils.trace.frame_proxy import get_exception_frames

from ..environment.default import __file__ as VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH
from ..environment.scarletio_coroutine import __file__ as VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH

from .assertion_conditional_base import __file__ as VAMPYTEST_ASSERTION_CONDITION_BASE_FILE_PATH
from .assertion_instance import __file__ as VAMPYTEST_ASSERTION_INSTANCE_FILE_PATH
from .assertion_raising import __file__ as VAMPYTEST_ASSERTION_RAISING_FILE_PATH
from .assertion_subtype import __file__ as VAMPYTEST_ASSERTION_SUBTYPE_FILE_PATH


def _ignore_assertion_frames(frame):
    """
    Ignores the frame where assertions are done.
    
    Parameters
    ----------
    frame : ``frameProxyBase``
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
    
    if file_name == VAMPYTEST_ASSERTION_CONDITION_BASE_FILE_PATH:
        if name == '__call__':
            if line == 'return type_.__new__(type_, *positional_parameters, **keyword_parameter).invoke()':
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
            if line == 'return self.invoke()':
                should_show_frame = False
    
    elif file_name == VAMPYTEST_ASSERTION_RAISING_FILE_PATH:
        if name == '__exit__':
            if line == 'raise AssertionException(self)':
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
    __slots__ = ('assertion',)
    __init__ = object.__init__
    
    def __new__(cls, assertion):
        """
        Creates a new condition exception.
        
        Parameters
        ----------
        assertion : ``AssertionBase``
            The failed assertion.
        """
        self = BaseException.__new__(cls, assertion)
        self.assertion = assertion
        return self
    
    
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
        frames = get_exception_frames(self)
        failure_message_parts.append('\n')
        render_frames_into(frames, failure_message_parts, filter = _ignore_assertion_frames)
        failure_message_parts.append('\n')
        self.assertion.render_failure_message_parts_into(failure_message_parts)
        return failure_message_parts
