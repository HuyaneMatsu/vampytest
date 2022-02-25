__all__ = ('WrapperSkip',)

from .wrapper_base import WrapperBase

class WrapperSkip(WrapperBase):
    """
    Skips the test.

    Attributes
    ----------
    wrapped : `None`, `Any`
        The wrapped test.
    """
    __slots__ = ()
    
    def do_skip(self):
        """
        Whether the test should be skipped.
        
        Returns
        -------
        do_skip : `bool`
            Always returns true.
        """
        return True
