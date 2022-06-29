__all__ = ('AssertionException', )

from scarletio.utils.trace import _get_exception_frames, render_frames_into


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
        failure_message_parts.append('\n')
        render_frames_into(_get_exception_frames(self)[1:-2], failure_message_parts)
        failure_message_parts.append('\n')
        self.assertion.render_failure_message_parts_into(failure_message_parts)
        return failure_message_parts
