__all__ = ('TestCase', )

import reprlib

from .handle import Handle
from .helpers import hash_object
from .result import ResultGroup
from .wrappers import WrapperBase

from scarletio import RichAttributeErrorBaseType


class TestCase(RichAttributeErrorBaseType):
    """
    Represents a test.
    
    Attributes
    ----------
    import_route : `str`
        Import route to the test's file.
    name : `str`
        The test's name.
    test : `callable`, ``WrapperBase``
        The test itself, or the wrapped test.
    wrapper : `None`, ``WrapperBase``
        Wrappers containing the test if any.    
    """
    __slots__ = ('import_route', 'name', 'test', 'wrapper')
    
    def __new__(cls, import_route, name, test):
        """
        Creates a new test case.
        
        Parameters
        ----------
        import_route : `str`
            Import route to the test's file.
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
        self.import_route = import_route
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
            repr_parts.append(', wrapper=')
            repr_parts.append(repr(self.wrapper))
        
        if self.do_skip():
            repr_parts.append(', skipped')
        
        if self.do_revert():
            repr_parts.append(', reverted')
        
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
    
    
    def do_revert(self):
        """
        Returns whether the test's result should be reverted.
        
        Returns
        -------
        do_revert : `bool`
        """
        wrapper = self.wrapper
        if wrapper is None:
            return False
        
        return wrapper.do_revert()
    
    
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
    
    
    def invoke(self, environment_manager):
        """
        Invokes the test case.
        
        Parameters
        ----------
        environment_manager : ``EnvironmentManager``
            Testing environment manager.
        
        Returns
        -------
        test_result : ``Result``
        """
        test_result_group = ResultGroup(self)
        conflict = self.check_conflicts()
        if (conflict is not None):
            return test_result_group.with_conflict(conflict)
        
        if self.do_skip():
            return test_result_group.as_skipped()
        
        for handler in self._iter_handles():
            test_result = handler.invoke(environment_manager)
            test_result_group = test_result_group.with_result(test_result)
        
        return test_result_group
    
    
    def _iter_handles(self):
        """
        Iterates over the test handles of the test case.
        
        This method is an iterable generator.
        
        Yields
        ------
        handle : ``Handle``
        """
        wrapper = self.wrapper
        if (wrapper is None):
            wrapper_groups = None
            environments = None
        
        else:
            wrapper_groups = set()
            
            environment_wrappers = [*wrapper.iter_environments()]
            if environment_wrappers:
                environments = tuple(environment_wrappers)
            else:
                environments = None
            
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
            yield Handle(self, test, None, environments)
        
        else:
            for wrapper_group in wrapper_groups:
                if (wrapper_group is not None):
                    wrapper_group = tuple(wrapper_group)
                
                yield Handle(self, test, wrapper_group, environments)
