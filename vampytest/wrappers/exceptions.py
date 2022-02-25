__all__ = ()

class WrapperConflict(BaseException):
    """
    Raised when 2 wrappers have conflict with each other.
    
    Attributes
    ----------
    wrappers : `tuple` (``WrapperBase``, ``WrapperBase``)
        The wrappers with the conflict.
    reason : `str`
        The reason why the two wrappers are incompatible.
    """
    def __init__(self, wrapper_1, wrapper_2, reason):
        """
        Creates a new wrapper conflict exception.
        
        Parameters
        ----------
        wrapper_1 : ``WrapperBase``
            Wrapper one with teh conflict.
        wrapper_2 : ``WrapperBase``
            Wrapper two with the conflict.
        reason : `str`
            The reason why the two wrappers are incompatible.
        """
        self.wrappers = wrapper_1, wrapper_2
        self.reason = reason
        BaseException.__init__(self, wrapper_1, wrapper_2, reason)
