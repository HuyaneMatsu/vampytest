__all__ = ()

import sys
from os import get_terminal_size

from scarletio import RichAttributeErrorBaseType


DEFAULT_BREAK_LINE_LENGTH = 60


class OutputWriter(RichAttributeErrorBaseType):
    """
    Test output writer.
    
    Attributes
    ----------
    _last_chunk_break_line : `bool`
        Whether the last written line was a break line.
    _last_write_ended_with_linebreak : `bool`
        Whether the last write ended with a linebreak.
    file : `io-like`
        object writable object.
    """
    def __new__(cls, file = None):
        """
        Creates a new test output writer.
        
        Parameters
        ----------
        file : `None`, `io-like` = `None`, Optional
            Writable object. If not given defaults to `sys.stdout`.
        """
        if file is None:
            file = sys.stdout
        
        self = object.__new__(cls)
        self._last_chunk_break_line = False
        self._last_write_ended_with_linebreak = False
        self.file = file
        return self
    
    
    def write_break_line(self, character = '='):
        """
        Writes a break line.
        
        Parameters
        ----------
        character : `str` = `'='`, Optional
            The character to use.
        
        Returns
        -------
        written : `bool`
        """
        if self._last_chunk_break_line:
            return False
        
        if not self._last_write_ended_with_linebreak:
            self.file.write('\n')
        
        try:
            terminal_size = get_terminal_size()
        except OSError:
            break_line_length = DEFAULT_BREAK_LINE_LENGTH
        else:
            break_line_length = terminal_size.columns
        
        self.file.write(character * break_line_length)
        
        self._last_write_ended_with_linebreak = False
        self._last_chunk_break_line = True
        
        return True
    
    
    def write_line(self, string):
        """
        Writes the given line into the file.
        
        Returns
        -------
        written : `bool`
        """
        if not string:
            return False
        
        if (not self._last_write_ended_with_linebreak) and (not string.startswith('\n')):
            self.file.write('\n')
        
        self.file.write(string)
        
        self._last_write_ended_with_linebreak = string.endswith('\n')
        self._last_chunk_break_line = False
        
        return True
    
    
    def write(self, string):
        """
        Writes the given line into the file.
        
        Returns
        -------
        written : `bool`
        """
        if not string:
            return False
        
        if self._last_chunk_break_line:
            self.file.write('\n')
        
        self.file.write(string)
        
        self._last_write_ended_with_linebreak = False
        self._last_chunk_break_line = False
        
        return True
    
    
    def end_line(self):
        """
        Ends the current line.
        
        Returns
        -------
        written : `bool`
        """
        if self._last_write_ended_with_linebreak:
            written = False
        
        else:
            self.file.write('\n')
            written = True
        
        self._last_write_ended_with_linebreak = True
        self._last_chunk_break_line = False
        
        return written
    
    
    def __del__(self):
        """Clears up the file of the output writer"""
        
        try:
            file = self.file
            
            flusher = getattr(file, 'flush', None)
            if (flusher is not None):
                try:
                    flusher()
                except NotImplementedError:
                    pass
            
            closer = getattr(file, 'close', None)
            if (closer is not None):
                try:
                    closer()
                except NotImplementedError:
                    pass
        
        finally:
            # Clear up self even if exception occurs.
            self = None
