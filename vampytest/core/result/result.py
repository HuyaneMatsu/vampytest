__all__ = ('Result',)

from scarletio import RichAttributeErrorBaseType, export

from .failures import FailureAsserting, FailureRaising, FailureReturning, get_reversed_failure_message


@export
class Result(RichAttributeErrorBaseType):
    """
    Represents a test's result.
    
    Attributes
    ----------
    handle : ``Handle``
        The test's handle running the test.
    failures : `None`, `list` of ``FailureBase``
        Test failures.
    reversed : `bool`
        Whether the test result is reversed.
    """
    __slots__ = ('handle', 'failures', 'reversed')
    
    def __new__(cls, handle):
        """
        Creates a new test result.
        
        Parameters
        ----------
        handle : ``Handle``
            The test's handle running the test.
        """
        self = object.__new__(cls)
        
        self.handle = handle
        self.failures = None
        self.reversed = False
        
        return self
    
    
    def __repr__(self):
        """Returns the test result's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        failures = self.failures
        if (failures is None):
            repr_parts.append(' passed')
        
        else:
            repr_parts.append(' failures = ')
            repr_parts.append(repr(failures))
        
        if self.reversed:
            repr_parts.append(', reversed')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
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
        self : ``Result``
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
        self : ``Result``
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
        self : ``Result``
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
    
    
    def is_failed(self):
        """
        Returns whether the test result failed.
        
        Returns
        -------
        is_failed : `bool`
        """
        return (self.failures is None) == self.reversed
    
    
    def is_passed(self):
        """
        Returns whether the test result passed.
        
        Returns
        -------
        is_failed : `bool`
        """
        return (self.failures is None) != self.reversed
    
    
    def iter_failure_message(self):
        """
        Returns the failure message of the test case.
        
        This method is an iterable generator.
        
        Yields
        -------
        failure_message : `str`
        """
        failures = self.failures
        if self.reversed:
            if (failures is None):
                yield get_reversed_failure_message(self.handle)
        
        else:
            if (failures is not None):
                for failure in failures:
                    yield failure.get_failure_message()
    
    
    def reverse(self):
        """
        Reverses the result.
        """
        self.reversed = True
