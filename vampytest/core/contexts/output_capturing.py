__all__ = ('ContextOutputCapturing',)

import sys
from io import StringIO

from scarletio import copy_docs

from .base import ContextBase


class ContextOutputCapturing(ContextBase):
    """
    Captures output.

    Attributes
    ----------
    standard_error_stream : `None`, `io-like`
        Standard error stream.
    standard_output_stream : `None`, `io-like`
        Standard output stream.
    stream : `None`, ``StringIO``
        Stream to capture stdout and stderr into.
    """
    __slots__ = ('standard_error_stream', 'standard_output_stream', 'stream')
    
    def __new__(cls):
        """
        Creates a new test context.
        """
        self = object.__new__(cls)
        self.stream = None
        self.standard_error_stream = None
        self.standard_output_stream = None
        return self
    
    
    @copy_docs(ContextBase.start)
    def start(self):
        stream = StringIO()
        self.stream = stream
        self.standard_output_stream = sys.stdout
        self.standard_error_stream = sys.stderr
        sys.stdout = stream
        sys.stderr = stream
    
    
    @copy_docs(ContextBase.close)
    def close(self, result):
        stream = self.stream
        if stream is None:
            # Was not started
            return
        
        sys.stdout = self.standard_output_stream
        sys.stderr = self.standard_error_stream
        self.standard_output_stream = None
        self.standard_error_stream = None
        
        if (result is not None):
            output = stream.getvalue()
            if output:
                result.with_output(output)
