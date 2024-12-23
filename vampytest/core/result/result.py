__all__ = ('Result',)

from scarletio import RichAttributeErrorBaseType, export

from .reports import (
    ReportFailureAsserting, ReportFailureParameterMismatch, ReportFailureRaising, ReportFailureReturning, ReportOutput
)


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
    reports : `None`, `list` of ``ReportBase``
        Test reports.
    reversed : `bool`
        Whether the test result is reversed.
    skipped : `bool`
        Whether the test is skipped.
    
    Utility Methods
    - ``.is_skipped``
    - ``.is_passed``
    - ``.is_failed``
    - ``.is_conflicted``
    - ``.is_informal``
    - ``.iter_report_messages``
    """
    __slots__ = ('case', 'conflict', 'continuous', 'handle', 'reports', 'reversed', 'skipped')
    
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
        self.reports = None
        self.reversed = case.do_reverse()
        self.skipped = False
        return self
    
    
    def __repr__(self):
        """Returns the test result's representation."""
        repr_parts = ['<', type(self).__name__]
        
        
        conflict = self.conflict
        if (conflict is None):
            field_added = False
        
        else:
            repr_parts.append(' conflict = ')
            repr_parts.append(repr(repr_parts))
            field_added = True
        
        reports = self.reports
        if (reports is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' reports = ')
            repr_parts.append(repr(reports))
        
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
    
    
    def with_exception(self, expected_exceptions, accept_subtypes, received_exception):
        """
        Adds unexpected exception as test result.
        
        Parameters
        ----------
        expected_exceptions : `None | set<type<BaseException> | instance<BaseException>>`
            A set of the expected exceptions.
        
        accept_subtypes : `bool`
            Whether exception subclasses are allowed
        
        received_exception : `None | BaseException`
            The received exception.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        report = ReportFailureRaising(expected_exceptions, accept_subtypes, received_exception)
        self._add_report(report)
        return self
    
    
    def with_return(self, expected_value, received_value):
        """
        Adds return value mismatch as test result.
        
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
        report = ReportFailureReturning(expected_value, received_value)
        self._add_report(report)
        return self
    
    
    def with_assertion(self, assertion_exception):
        """
        Adds assertion failing as test result.
        
        Parameters
        ----------
        assertion_exception : ``AssertionException``
            The failed assertion.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        report = ReportFailureAsserting(assertion_exception)
        self._add_report(report)
        return self
    
    
    def with_parameter_mismatch(self, parameter_mismatch):
        """
        Adds a parameter mismatch as a test result.
        
        Parameters
        ----------
        parameter_mismatch : ``ParameterMismatch``
            The parameter mismatch to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        report = ReportFailureParameterMismatch(parameter_mismatch)
        self._add_report(report)
        return self
    
    
    def with_output(self, output):
        """
        Adds captured output as test result. 
        
        Parameters
        ----------
        output : `str`
            Output to add.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        report = ReportOutput(output)
        self._add_report(report)
        return self
    
    
    def _add_report(self, report):
        """
        Ads a report to the test result.
        
        Parameters
        ----------
        report : ``ReportBase``
            The test report to add.
        """
        reports = self.reports
        if (reports is None):
            reports = []
            self.reports = reports
        
        reports.append(report)
    
    
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
        
        return (self.get_failure_report() is None) != self.reversed
    
    
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
        
        return (self.get_failure_report() is None) == self.reversed
    
    
    def is_conflicted(self):
        """
        Returns whether the respective test case conflicted.
        
        Returns
        -------
        is_conflicted : `bool`
        """
        return (self.conflict is not None)
    
    
    def is_informal(self):
        """
        Returns whether the test result holds only informal results.
        
        Returns
        -------
        is_informal : `bool`
        """
        if self.skipped:
            return False
        
        if (self.conflict is not None):
            return False
        
        has_informal = False
        
        for report in self.iter_reports():
            if report.is_failure():
                return False
            
            if report.is_informal():
                has_informal = True
        
        return has_informal
        
    
    def is_last(self):
        """
        Returns whether the result is the last of the test case. Can be used when rendering test tree.
        
        Returns
        -------
        is_last : `bool`
        """
        return (not self.continuous)
    
    
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
    
    
    def iter_reports(self):
        """
        Iterates over the reports of the test result.
        
        Yields
        ------
        report : ``ReportBase``
        """
        reports = self.reports
        if reports is not None:
            yield from reports
    
    
    def get_failure_report(self):
        """
        Gets the first failure report.
        
        Returns
        -------
        report : `None`, ``ReportBase``
        """
        for report in self.iter_reports():
            if report.is_failure():
                return report
    
    
    def get_output_report(self):
        """
        Gets the first output report.
        
        Returns
        -------
        report : `None`, ``ReportOutput``
        """
        for report in self.iter_reports():
            if isinstance(report, ReportOutput):
                return report
