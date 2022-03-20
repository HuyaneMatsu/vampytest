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
