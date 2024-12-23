from ....assertions import assert_eq, assert_in, assert_instance

from ..failure_raising import ReportFailureRaising


def _assert_fields_set(report):
    """
    Asserts whether the report has all of its attributes set.
    
    Parameters
    ----------
    report : ``ReportFailureRaising``
        The report to check.
    """
    assert_instance(report, ReportFailureRaising)
    assert_instance(report.accept_subtypes, bool)
    assert_instance(report.expected_exceptions, set, nullable = True)
    assert_instance(report.exception_received, BaseException, nullable = True)


def test__ReportFailureRaising__new():
    """
    Tests whether ``ReportFailureRaising.__new__`` works as intended.
    """
    expected_exceptions = {ValueError(), }
    accept_subtypes = True
    exception_received = IndexError(5)
    
    report = ReportFailureRaising(expected_exceptions, accept_subtypes, exception_received)
    _assert_fields_set(report)
    
    assert_eq(report.expected_exceptions, expected_exceptions)
    assert_eq(report.accept_subtypes, accept_subtypes)
    assert_eq(report.exception_received, exception_received)


def test__ReportFailureRaising__repr():
    """
    Tests whether ``ReportFailureRaising.__repr__`` works as intended.
    """
    expected_exceptions = {ValueError(), }
    accept_subtypes = True
    exception_received = IndexError(5)
    
    report = ReportFailureRaising(expected_exceptions, accept_subtypes, exception_received)
    
    output = repr(report)
    
    assert_instance(output, str)
    assert_in(type(report).__name__, output)
    assert_in(f'expected_exceptions = {expected_exceptions!r}', output)
    assert_in(f'accept_subtypes = {accept_subtypes!r}', output)
    assert_in(f'exception_received = {exception_received!r}', output)


def test__ReportFailureRaising__is_failure():
    """
    Tests whether ``ReportFailureRaising.is_failure`` works as intended.
    """
    expected_exceptions = {ValueError(), }
    accept_subtypes = True
    exception_received = IndexError(5)
    
    report = ReportFailureRaising(expected_exceptions, accept_subtypes, exception_received)
    
    output = report.is_failure()
    assert_instance(output, bool)
    assert_eq(output, True)


def test__ReportFailureRaising__is_informal():
    """
    Tests whether ``ReportFailureRaising.is_informal`` works as intended.
    """
    expected_exceptions = {ValueError(), }
    accept_subtypes = True
    exception_received = IndexError(5)
    
    report = ReportFailureRaising(expected_exceptions, accept_subtypes, exception_received)
    
    output = report.is_informal()
    assert_instance(output, bool)
    assert_eq(output, False)
