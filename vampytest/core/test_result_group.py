__all__ = ('TestResultGroup',)

from scarletio import RichAttributeErrorBaseType


class TestResultGroup(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    conflict : `None`, ``WrapperConflict``
        Conflicts between test wrappers.
    results : `None`, `list` of ``TestResult``
        The results of the ran test(s).
    skipped : `bool`
        Whether the test is skipped.
    """
    __slots__ = ('conflict', 'results', 'skipped')
    
    def __new__(cls, *, conflict=None, skipped=False):
        """
        Creates a new test result group.
        
        Parameters
        ----------
        conflict : `None`, ``WrapperConflict``, Optional (Keyword only)
            Conflicts between test wrappers.
        skipped : `bool`, Optional (Keyword only)
            Whether the test is skipped.
        """
        self = object.__new__(cls)
        self.conflict = conflict
        self.results = None
        self.skipped = skipped
        return self
    
    
    def __repr__(self):
        """Returns the representation of the test result group."""
        repr_parts = ['<', self.__class.__name__]
        
        while True:
            conflict = self.conflict
            if (conflict is not None):
                repr_parts.append(' conflict=')
                repr_parts.append(repr(repr_parts))
                break
            
            results = self.results
            if (results is not None):
                repr_parts.append(' results=')
                repr_parts.append(repr(results))
                break
            
            skipped = self.skipped
            if skipped:
                repr_parts.append(' skipped=')
                repr_parts.append(repr(skipped))
                break
            
            # no more cases
            break
        
        repr_parts.append('>')
        return '\n'.join(repr_parts)


    def add(self, test_result):
        """
        Adds a test result to the test result group.
        
        Parameters
        ----------
        test_result : ``TestResult``
            The test result to add.
        """
        results = self.results
        if (results is None):
            results = []
            self.results = results
        
        results.append(test_result)
    
