__all__ = ('CaptureOutputContextManager',)

import sys
from io import StringIO

from scarletio import RichAttributeErrorBaseType


class CaptureOutputContextManager(RichAttributeErrorBaseType):
    """
    Captures stdout and stderr.
    
    Attributes
    ----------
    _standard_error_stream : `None`, `io-like`
        Standard error stream.
    _standard_output_stream : `None`, `io-like`
        Standard output stream.
    _stream : `None`, ``StringIO``
        Stream to capture stdout and stderr into.
    """
    __slots__ = ('_standard_error_stream', '_standard_output_stream', '_stream')
    
    def __new__(cls):
        """
        Creates a new output capture instance.
        """
        stream = StringIO()
        self = object.__new__(cls)
        self._standard_error_stream = None
        self._standard_output_stream = None
        self._stream = stream
        return self
    
    
    def __enter__(self):
        """Enters the context manager."""
        if (self._standard_output_stream is not None) or (self._standard_error_stream is not None):
            raise RuntimeError('Context manager already entered.')
        
        self._standard_output_stream = sys.stdout
        self._standard_error_stream = sys.stderr
        stream = self._stream
        sys.stdout = stream
        sys.stderr = stream
        return self
    
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        """Exists the context manager."""
        if (self._standard_output_stream is None) and (self._standard_error_stream is None):
            # Was not started
            return False
        
        sys.stdout = self._standard_output_stream
        sys.stderr = self._standard_error_stream
        self._standard_output_stream = None
        self._standard_error_stream = None
        return False
    
    
    def get_value(self):
        """
        Gets the value written since last call.
        
        Returns
        -------
        value : `str`
        """
        stream = self._stream
        position = stream.tell()
        stream.seek(0)
        value = stream.read(position)
        stream.seek(0)
        return value
