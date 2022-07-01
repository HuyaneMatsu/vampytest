__all__ = ('ResultGroup',)

from scarletio import RichAttributeErrorBaseType


class ResultGroup(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    case : ``TestCase``
        The parent test case creating this test group.
    conflict : `None`, ``WrapperConflict``
        Conflicts between test wrappers.
    results : `None`, `list` of ``Result``
        The results of the ran test(s).
    skipped : `bool`
        Whether the test is skipped.
    
    Utility Methods
    - ``.is_skipped``
    - ``.is_passed``
    - ``.is_failed``
    - ``.iter_failure_messages``
    
    """
    __slots__ = ('case', 'conflict', 'results', 'skipped')
    
    def __new__(cls, case):
        """
        Creates a new test result group.
        
        Parameters
        ----------
        case : ``TestCase``
            The parent test case creating this test group.
        """
        self = object.__new__(cls)
        self.case = case
        self.conflict = None
        self.results = None
        self.skipped = False
        return self
    
    
    def with_conflict(self, conflict):
        """
        Adds the conflict to the test result group.
        
        Parameters
        ----------
        conflict : ``WrapperConflict``
            Conflicts between test wrappers.
            
        Returns
        -------
        self : ``ResultGroup``
        """
        self.conflict = conflict
        return self
    
    
    def as_skipped(self):
        """
        Marks the test result as skipped.
        
        Returns
        -------
        self : ``ResultGroup``
        """
        self.skipped = True
        return self
    
    
    def __repr__(self):
        """Returns the representation of the test result group."""
        repr_parts = ['<', self.__class__.__name__]
        
        
        
        conflict = self.conflict
        if (conflict is None):
            field_added = False
        
        else:
            repr_parts.append(' conflict=')
            repr_parts.append(repr(repr_parts))
            field_added = True
        
        
        results = self.results
        if (results is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' results=')
            repr_parts.append(repr(results))
        
        
        if self.skipped:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' skipped')
        
        
        if self.case.do_revert():
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' reverted')
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def with_result(self, test_result):
        """
        Adds a test result to the test result group.
        
        Parameters
        ----------
        test_result : ``Result``
            The test result to add.
        
        Returns
        -------
        self : ``ResultGroup``
        """
        if self.case.do_revert():
            test_result.revert()
        
        results = self.results
        if (results is None):
            results = []
            self.results = results
        
        results.append(test_result)
        
        return self
    
    
    def is_skipped(self):
        """
        Returns whether the represented test case was skipped.
        
        Returns
        -------
        is_skipped : `bool`
        """
        return self.skipped
    
    
    def is_passed(self):
        """
        Returns whether the respective test case passed.
        
        Returns
        -------
        is_passed : `bool`
        """
        if self.skipped:
            return True
        
        if (self.conflict is not None):
            return False
        
        results = self.results
        if (results is not None):
            for result in results:
                if result.is_failed():
                    return False
        
        return True
    
    
    def is_failed(self):
        """
        Returns whether the respective test case failed.
        
        Returns
        -------
        is_failed : `bool`
        """
        if self.skipped:
            return False
        
        if (self.conflict is not None):
            return True
        
        results = self.results
        if (results is not None):
            for result in results:
                if result.is_failed():
                    return True
        
        return False
    
    
    def iter_failure_messages(self):
        """
        Iterates over the failure messages of the test group.
        
        This method is an iterable generator.
        
        Yields
        -------
        failure_message : `str`
        """
        conflict = self.conflict
        if (conflict is not None):
            yield conflict.get_failure_message()
        
        results = self.results
        if (results is not None):
            for result in results:
                yield from result.iter_failure_message()
