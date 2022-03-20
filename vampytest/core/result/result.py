__all__ = ('Result',)

from .failures import FailureAsserting, FailureRaising, FailureReturning

from scarletio import RichAttributeErrorBaseType


class Result(RichAttributeErrorBaseType):
    """
    Represents a test's result.
    
    Attributes
    ----------
    handle : ``Handle``
        The test's handle running the test.
    failures : `None`, `list` of ``FailureBase``
        test failures.
    """
    __slots__ = ('handle', 'failures')
    
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
        
        return self
    
    
    def __repr__(self):
        """Returns the test result's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        failures = self.failures
        if (failures is not None):
            repr_parts.append(' failures=')
            repr_parts.append(repr(failures))
        
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
        expected_value : `Any`
            The expected return value.
        received_value : `Any`
            The received return value.
        
        Returns
        -------
        self : ``Result``
        """
        failure = FailureReturning(self.handle, expected_value, received_value)
        self._add_failure(failure)
        
        return self
    
    
    def with_assertion(self, assertion):
        """
        Sets assertion as test result.
        
        Parameters
        ----------
        assertion : ``AssertionBase``
            The failed assertion.
        
        Returns
        -------
        self : ``Result``
        """
        failure = FailureAsserting(self.handle, assertion)
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
        return (self.failures is not None)
    
    
    def is_passed(self):
        """
        Returns whether the test result passed.
        
        Returns
        -------
        is_failed : `bool`
        """
        return (self.failures is None)
    
    
    def iter_failure_message(self):
        """
        Returns the failure message of the test case.
        
        This method is an iterable generator.
        
        Yields
        -------
        failure_message : `str`
        """
        failures = self.failures
        if (failures is not None):
            for failure in failures:
                yield failure.get_failure_message()
