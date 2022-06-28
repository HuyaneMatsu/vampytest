__all__ = ('AssertionException', )

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
    
    
    def render_into(self, failure_message_parts):
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
        
        
        return failure_message_parts
