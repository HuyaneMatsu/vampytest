__all__ = ('WrapperSkipConditional', )

from .wrapper_skip import WrapperSkip


class WrapperSkipConditional(WrapperSkip):
    """
    Skips the test.

    Attributes
    ----------
    wrapped : `None`, `Any`
        The wrapped test.
    """
    __slots__ = ('skip', )
    
    def __new__(cls, skip):
        """
        Creates a new conditional skip wrapper.
        
        Parameters
        ----------
        skip : `bool`
            Whether the test should be skipped.
        """
        skip = bool(skip)
        
        self = WrapperSkip.__new__(cls)
        self.skip = skip
        return self
    
    
    def do_skip(self):
        """
        Whether the test should be skipped.
        
        Returns
        -------
        do_skip : `bool`
        """
        return self.skip
