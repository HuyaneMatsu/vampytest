__all__ = ('TestLoadingError',)


class TestLoadingError(BaseException):
    """
    Raised when exception occurs when a test file is loaded.
    
    Attributes
    ----------
    source_exception : `BaseException`
        The source exception.
    """
    def __init__(self, source_exception):
        self.source_exception = source_exception
        BaseException.__init__(self, source_exception)
