__all__ = ('TestCase', )

import reprlib

from .helpers import hash_object
from .wrappers import WrapperBase
from .test_handle import TestHandle
from .test_result_group import TestResultGroup

from scarletio import RichAttributeErrorBaseType


class TestCase(RichAttributeErrorBaseType):
    """
    Represents a test.
    
    Attributes
    ----------
    name : `str`
        The test's name.
    test : `callable`, ``WrapperBase``
        The test itself, or the wrapped test.
    wrapper : `None`, ``WrapperBase``
        Wrappers containing the test if any.
    """
    __slots__ = ('name', 'test', 'wrapper')
    
    def __new__(cls, name, test):
        """
        Creates a new test case.
        
        Parameters
        ----------
        name : `str`
            The test's name.
        test : `callable`, ``WrapperBase``
            The test itself, or the wrapped test.
        """
        if isinstance(test, WrapperBase):
            wrapper = test
            test = test.unbind_test()
        else:
            wrapper = None
            test = test
        
        self = object.__new__(cls)
        self.name = name
        self.test = test
        self.wrapper = wrapper
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two test cases are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return False
    
    
    def __hash__(self):
        """Returns the test case's hash value."""
        hash_value = 0
        
        hash_value ^= hash(self.name)
        hash_value ^= hash_object(self.test)
        
        wrapper = self.wrapper
        if (wrapper is not None):
            hash_value ^= hash(wrapper)
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the test case's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        repr_parts.append(', test=')
        repr_parts.append(reprlib.repr(self.test))
        
        wrapper = self.wrapper
        if (wrapper is not None):
            repr_parts.append(' wrapper=')
            repr_parts.append(repr(self.wrapper))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def do_skip(self):
        """
        Returns whether the test should be skipped.
        
        Returns
        -------
        do_skip : `bool`
        """
        wrapper = self.wrapper
        if wrapper is None:
            return False
        
        return wrapper.do_skip()
    
    
    def check_conflicts(self):
        """
        Checks the test case's wrappers' conflicts.
        
        Returns
        ------
        wrapper_conflict: `None`, ``WrapperConflict``
        """
        wrapper = self.wrapper
        if (wrapper is not None):
            return wrapper.check_conflicts()
    
    
    def invoke(self):
        """
        Invokes the test case.
        
        Returns
        -------
        test_result : ``TestResult``
        """
        conflict = self.check_conflicts()
        if (conflict is not None):
            return TestResultGroup(conflict=conflict)
        
        if self.do_skip():
            return TestResultGroup(skipped=True)
        
        test_result_group = TestResultGroup()
        
        for test_handler in self._iter_test_handles():
            test_result = test_handler.invoke()
            test_result_group.add(test_result)
        
        return test_result_group
    
    
    def _iter_test_handles(self):
        """
        Iterates over the test handles of the test case.
        
        This method is an iterable generator.
        
        Yields
        ------
        test_handle : ``TestHandle``
        """
        wrapper = self.wrapper
        if (wrapper is None):
            wrapper_groups = None
        
        else:
            wrapper_groups = set()
            
            wrappers = [wrapper for wrapper in wrapper.iter_wrappers() if not wrapper.is_ignored_when_testing()]
            
            while wrappers:
                wrapper_to_check = wrappers.pop()
                wrapper_group = [wrapper_to_check]
                
                for wrapper in wrappers:
                    if wrapper.is_mutually_exclusive_with(wrapper_to_check):
                        continue
                    
                    if wrapper_to_check.is_mutually_exclusive_with(wrapper):
                        continue
                    
                    wrapper_group.append(wrapper_to_check)
                    continue
                
                wrapper_group = frozenset(wrapper_group)
                wrapper_groups.add(wrapper_group)
            
            if not wrapper_groups:
                wrapper_groups = None
        
        test = self.test
        
        if (wrapper_groups is None):
            yield TestHandle(test)
        
        else:
            for wrapper_group in wrapper_groups:
                yield TestHandle(test, wrapper_group)
