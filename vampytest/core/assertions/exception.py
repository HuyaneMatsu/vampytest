__all__ = ('AssertionException', )

from scarletio import export
from ..environment.default import __file__ as VAMPYTEST_ENVIRONMENT_DEFAULT_FILE_PATH
from ..environment.scarletio_coroutine import __file__ as VAMPYTEST_ENVIRONMENT_SCARLETIO_COROUTINE_FILE_PATH

from .assertion_conditional_base import __file__ as VAMPYTEST_ASSERTION_CONDITION_BASE_FILE_PATH
from .assertion_instance import __file__ as VAMPYTEST_ASSERTION_INSTANCE_FILE_PATH
from .assertion_raising import __file__ as VAMPYTEST_ASSERTION_RAISING_FILE_PATH
from .assertion_subtype import __file__ as VAMPYTEST_ASSERTION_SUBTYPE_FILE_PATH
from .top_level import __file__ as VAMPYTEST_TOP_LEVEL_FILE_PATH


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
    
    if file_name == VAMPYTEST_TOP_LEVEL_FILE_PATH:
        if name in (
            'assert_contains', 'assert_equals', 'assert_false', 'assert_identical', 'assert_instance',
            'assert_not_contains', 'assert_not_equals', 'assert_not_identical', 'assert_subtype', 'assert_true'
        ):
            if line == 'return assertion.invoke()':
                should_show_frame = False
    
    elif file_name == VAMPYTEST_ASSERTION_CONDITION_BASE_FILE_PATH:
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
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # assertion
        repr_parts.append(' assertion = ')
        repr_parts.append(repr(self.assertion))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
