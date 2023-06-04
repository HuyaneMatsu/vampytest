__all__ = ('Result',)

from scarletio import RichAttributeErrorBaseType, export

from .failures import FailureAsserting, FailureRaising, FailureReturning, get_reversed_failure_message


@export
class Result(RichAttributeErrorBaseType):
    """
    Represents a test's result.
    
    Attributes
    ----------
    case : ``TestCase``
        The parent test case creating this test group.
    conflict : `None`, ``WrapperConflict``
        Conflicts between test wrappers.
    continuous : `bool`
        Whether this is is not the last test of the case.
    handle : ``Handle``
        The test's handle running the test.
    failures : `None`, `list` of ``FailureBase``
        Test failures.
    reversed : `bool`
        Whether the test result is reversed.
    skipped : `bool`
        Whether the test is skipped.
    
    Utility Methods
    - ``.is_skipped``
    - ``.is_passed``
    - ``.is_failed``
    - ``.is_conflicted``
    - ``.iter_failure_messages``
    """
    __slots__ = ('case', 'conflict', 'continuous', 'handle', 'failures', 'reversed', 'skipped')
    
    def __new__(cls, case):
        """
        Creates a new test result.
        
        Parameters
        ----------
        case : ``TestCase``
            The parent test case creating this test group.
        """
        self = object.__new__(cls)
        self.case = case
        self.conflict = None
        self.continuous = False
        self.handle = None
        self.failures = None
        self.reversed = case.do_reverse()
        self.skipped = False
        return self
    
    
    def __repr__(self):
        """Returns the test result's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        
        conflict = self.conflict
        if (conflict is None):
            field_added = False
        
        else:
            repr_parts.append(' conflict = ')
            repr_parts.append(repr(repr_parts))
            field_added = True
        
        failures = self.failures
        if (failures is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' failures = ')
            repr_parts.append(repr(failures))
        
        if self.reversed:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' reversed')
        
        if self.skipped:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' skipped')
        
        if self.continuous:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' continuous')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def with_handle(self, handle):
        """
        Sets handle.
        
        Parameters
        ----------
        handle : ``Handle``
            The test's handle running the test.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.handle = handle
        return self
    
    
    def with_conflict(self, conflict):
        """
        Adds the conflict to the test result.
        
        Parameters
        ----------
        conflict : ``WrapperConflict``
            Conflicts between test wrappers.
            
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.conflict = conflict
        return self
    
    
    def as_skipped(self):
        """
        Marks the test result as skipped.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.skipped = True
        return self
    
    
    def as_continuous(self):
        """
        Marks the test result as continuous.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self.continuous = True
        return self
    
    
    def with_exception(self, expected_exceptions, received_exception, exact_type):
        """
        Sets except result.
        
        Parameters
        ----------
        expected_exceptions : `None`, `set` of `BaseException`
            A set of the expected exceptions.
        received_exception : `None`, ``BaseException``
            The received exception.
        exact_type : `bool`
            Whether exception subclasses are disallowed.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        failure = FailureRaising(self.handle, expected_exceptions, received_exception, exact_type)
        self._add_failure(failure)
        
        return self
    
    
    def with_return(self, expected_value, received_value):
        """
        Sets return result.
        
        Parameters
        ----------
        expected_value : `object`
            The expected return value.
        received_value : `object`
            The received return value.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        failure = FailureReturning(self.handle, expected_value, received_value)
        self._add_failure(failure)
        
        return self
    
    
    def with_assertion(self, assertion_exception):
        """
        Sets assertion as test result.
        
        Parameters
        ----------
        assertion_exception : ``AssertionException``
            The failed assertion.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        failure = FailureAsserting(self.handle, assertion_exception)
        self._add_failure(failure)
        
        return self
    
    
    def _add_failure(self, failure):
        """
        Ads a failure to the test result.
        
        Parameters
        ----------
        failure : ``FailureBase``
            The test failure to add.
        """
        failures = self.failures
        if (failures is None):
            failures = []
            self.failures = failures
        
        failures.append(failure)
    
    
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
        Returns whether the test result passed.
        
        Returns
        -------
        is_failed : `bool`
        """
        if self.skipped:
            return True
        
        if (self.conflict is not None):
            return False
        
        return (self.failures is None) != self.reversed
    
    
    def is_failed(self):
        """
        Returns whether the test result failed.
        
        Returns
        -------
        is_failed : `bool`
        """
        if self.skipped:
            return False
        
        if (self.conflict is not None):
            return True
        
        
        return (self.failures is None) == self.reversed
    
    
    def is_conflicted(self):
        """
        Returns whether the respective test case conflicted.
        
        Returns
        -------
        is_conflicted : `bool`
        """
        return (self.conflict is not None)
    
    
    def is_last(self):
        """
        Returns whether the result is the last of the test case. Can be used when rendering test tree.
        
        Returns
        -------
        is_last : `bool`
        """
        return (not self.continuous)
    
    
    def iter_failure_messages(self):
        """
        Returns the failure message of the test case.
        
        This method is an iterable generator.
        
        Yields
        -------
        failure_message : `str`
        """
        conflict = self.conflict
        if (conflict is not None):
            yield conflict.get_failure_message()
        
        failures = self.failures
        if self.reversed:
            if (failures is None):
                yield get_reversed_failure_message(self.handle)
        
        else:
            if (failures is not None):
                for failure in failures:
                    yield failure.get_failure_message()
    
    
    def get_modifier_parameters(self):
        """
        Returns the test's modifier parameters.
        
        Returns
        -------
        modifier_parameters : `None | (None | list<object>, None | dict<str, object)`
        """
        handle = self.handle
        if handle is None:
            return None
        
        final_call_state = handle.final_call_state
        if final_call_state is None:
            return None
        
        if not final_call_state:
            return None
        
        return final_call_state.positional_parameters, final_call_state.keyword_parameters
