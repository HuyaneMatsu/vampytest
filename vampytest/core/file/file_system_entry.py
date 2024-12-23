__all__ = ('FileSystemEntry',)

from os import listdir as list_directory
from os.path import join as join_paths, isdir as is_directory, isfile as is_file

from scarletio import RichAttributeErrorBaseType, WeakReferer


PYTHON_EXTENSIONS = ('.py', '.pyd', '.pyc', '.so')


def is_python_file(path):
    """
    Returns whether the given path refers to a python file.
    
    Parameters
    ----------
    path : `str`
        Path to the file.
    
    Returns
    -------
    path : `str`
    """
    if is_file(path):
        return path
    
    if not path.endswith(PYTHON_EXTENSIONS):
        for extension in PYTHON_EXTENSIONS:
            file_path = path + extension
            if is_file(file_path):
                return file_path
    
    return None


class FileSystemEntry(RichAttributeErrorBaseType):
    __slots__ = (
        '__weakref__', '_directory', '_directory_path', '_entries', '_full_path', '_name', '_parent_reference',
        '_self_reference', '_used'
    )
        
    def __new__(cls, path, name, limit_lookup_to):
        """
        Creates a new File system entry.
        
        Parameters
        ----------
        path : `str`
            Path to the entry's directory.
        name : `str | None`
            The name of the entry.
        limit_lookup_to : `None | list<str>`
            Limits sub-directory lookups to only the given path.
        
        Returns
        -------
        entry : `None | instance<cls>`
        """
        full_path = join_paths(path, name)
        directory = is_directory(full_path)
        
        entries = None
        
        if directory:
            if (limit_lookup_to is None) or (not limit_lookup_to):
                for sub_name in sorted(list_directory(full_path)):
                    entry = cls(full_path, sub_name, None)
                    if entry is None:
                        continue
                    
                    if entries is None:
                        entries = []
                    
                    entries.append(entry)
            
            else:
                entry = cls(full_path, limit_lookup_to[0], limit_lookup_to[1:])
                if (entry is not None):
                    if entries is None:
                        entries = []
                    
                    entries.append(entry)
        else:
            file_path = is_python_file(full_path)
            if file_path is None:
                return None
            
            full_path = file_path
        
        self = object.__new__(cls)
        self._directory = directory
        self._directory_path = path
        self._entries = entries
        self._full_path = full_path
        self._name = name
        self._parent_reference = None
        self._self_reference = None
        self._used = 0
        
        for entry in self.iter_entries():
            entry.link_parent(self)
        
        return self
    
    
    def __bool__(self):
        """Returns whether the entry is used anywhere."""
        if self._used:
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the entry's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' path = ')
        repr_parts.append(repr(self.get_path()))
        
        repr_parts.append(', entry count: ')
        entries = self._entries
        if (entries is None):
            entry_count = 0
        else:
            entry_count = len(entries)
        repr_parts.append(repr(entry_count))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def mark_as_used(self):
        """
        Marks the file as used.
        """
        self._used += 1
        
        parent = self.get_parent()
        if (parent is not None):
            parent.mark_as_used()
    
    
    def get_path(self):
        """
        Returns the full path of the entry.
        
        Returns
        -------
        path : `str`
        """
        return self._full_path
    
    
    def get_self_reference(self):
        """
        Returns the a weak reference to self.
        
        Returns
        -------
        weak_reference : ``WeakReferer``
        """
        self_reference = self._self_reference
        if (self_reference is None):
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference
    
    
    def link_parent(self, parent):
        """
        Links the parent directory to self.
        
        Parameters
        ----------
        parent : ``FileSystemEntry``
            The parent to link.
        """
        self._parent_reference = parent.get_self_reference()
    
    
    def get_parent(self):
        """
        Returns the entry's parent.
        
        Returns
        -------
        parent : `None`, ``FileSystemEntry``
        """
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            return parent_reference()
    
    
    def is_last(self):
        """
        Returns whether the entry is last in it's parent.
        
        Returns
        -------
        is_last : `bool`
        """
        parent = self.get_parent()
        if parent is None:
            return True
        
        entries = parent._entries
        if (entries is None):
            return True
        
        if self is entries[-1]:
            return True
        
        return False
    
    
    def iter_parents(self):
        """
        Iterates over the parents of the entry.
        
        This method is an iterable generator.
        
        Yields
        ------
        parent : ``FileSystemEntry``
        """
        parent = self.get_parent()
        if (parent is not None):
            yield from parent.iter_parents()
            yield parent
    
    
    def iter_parents_skip_first(self):
        """
        Iterates over the parents of the entry. But skips the first!
        
        This method is an iterable generator.
        
        Yields
        ------
        parent : ``FileSystemEntry``
        
        Returns
        -------
        reached_end : `bool`
            Whether the parent reached the end.
        """
        parent = self.get_parent()
        if (parent is None):
            return True
        
        reached_end = yield from parent.iter_parents_skip_first()
        if (not reached_end):
            yield parent
        
        return False
    
    
    def has_parents(self):
        """
        Returns whether self has parents.
        
        Returns
        -------
        has_parents : `bool`
        """
        return self.get_parent() is not None
    
    
    def get_name(self):
        """
        Returns the entry's name.
        
        Returns
        -------
        name : `str`
        """
        return self._name
    
    
    def is_directory(self):
        """
        Returns whether self represents a directory.
        
        Returns
        -------
        is_directory : `bool`
        """
        return self._directory
    
    
    def is_file(self):
        """
        Returns whether self represents a file.
        
        Returns
        -------
        is_file : `bool`
        """
        return not self._directory
    
    
    def iter_entries(self):
        """
        Iterates over the sub entries.
        
        This method is an iterable generator.
        
        Yields
        ------
        parent : ``FileSystemEntry``
        """
        entries = self._entries
        if (entries is not None):
            yield from entries
    
    
    def purge(self):
        """
        Prunes all the sub members who are not used.
        
        Returns
        -------
        used : `bool`
        """
        if not self:
            return False
        
        entries = None
        
        for entry in self.iter_entries():
            if entry.purge():
                if entries is None:
                    entries = []
                
                entries.append(entry)
        
        self._entries = entries
        
        return True
    
    
    def render_into(self, into, *, name = None):
        """
        Renders the path access into the given list of strings.
        
        Parameters
        ----------
        into : `list` of `str`
            List to render self into.
        name : `None`, `str` = `None`, Optional (Keyword only)
            Custom name to use.
        
        Returns
        -------
        into : `list` of `str`
        """
        for parent in self.iter_parents_skip_first():
            if parent.is_last():
                into.append('   ')
            else:
                into.append('│  ')
        
        if self.has_parents():
            if self.is_last():
                into.append('└─ ')
            else:
                into.append('├─ ')
        
        if name is None:
            name = self._name
        
        into.append(name)
        into.append('\n')
        
        return into
    
    
    def render_custom_sub_directory_into(self, into, name, last):
        """
        Renders a custom sub directory.
        
        Parameters
        ----------
        into : `list` of `str`
            List to render self into.
        name : `str`
            The name of the sub-directory.
        last : `bool`
            Whether self is the last element on the line.
        
        Returns
        -------
        into : `list` of `str`
        """
        for parent in self.iter_parents_skip_first():
            if parent.is_last():
                into.append('   ')
            else:
                into.append('│  ')
        
        if self.has_parents():
            if self.is_last():
                into.append('   ')
            else:
                into.append('│  ')
        
        if last:
            into.append('└─ ')
        else:
            into.append('├─ ')
        
        into.append(name)
        into.append('\n')
        
        return into
