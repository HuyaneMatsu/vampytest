__all__ = ('AssertionException', )

class AssertionException(BaseException):
    """
    Raised when an exception fails.
    
    Attributes
    ----------
    condition : ``Condition``
        The failed condition.
    """
    def __init__(self, condition):
        """
        Creates a new condition exception.
        
        Parameters
        ----------
        condition : ``Condition``
            The failed condition.
        """
        self.condition = condition
        BaseException.__init__(self, condition)
