from ....assertions import assert_eq, assert_in, assert_instance

from ..failure_returning import ReportFailureReturning


def _assert_fields_set(report):
    """
    Asserts whether the report has all of its attributes set.
    
    Parameters
    ----------
    report : ``ReportFailureReturning``
        The report to check.
    """
    assert_instance(report, ReportFailureReturning)
    assert_instance(report.expected_value, object, nullable = True)
    assert_instance(report.received_value, object, nullable = True)


def test__ReportFailureReturning__new():
    """
    Tests whether ``ReportFailureReturning.__new__`` works as intended.
    """
    expected_value = 22
    received_value = 21
    
    report = ReportFailureReturning(expected_value, received_value)
    _assert_fields_set(report)
    
    assert_eq(report.expected_value, expected_value)
    assert_eq(report.received_value, received_value)


def test__ReportFailureReturning__repr():
    """
    Tests whether ``ReportFailureReturning.__repr__`` works as intended.
    """
    expected_value = 22
    received_value = 21
    
    report = ReportFailureReturning(expected_value, received_value)
    
    output = repr(report)
    
    assert_instance(output, str)
    assert_in(type(report).__name__, output)
    assert_in(f'expected_value = {expected_value!r}', output)
    assert_in(f'received_value = {received_value!r}', output)


def test__ReportFailureReturning__is_failure():
    """
    Tests whether ``ReportFailureReturning.is_failure`` works as intended.
    """
    expected_value = 22
    received_value = 21
    
    report = ReportFailureReturning(expected_value, received_value, )
    
    output = report.is_failure()
    assert_instance(output, bool)
    assert_eq(output, True)


def test__ReportFailureReturning__is_informal():
    """
    Tests whether ``ReportFailureReturning.is_informal`` works as intended.
    """
    expected_value = 22
    received_value = 21
    
    report = ReportFailureReturning(expected_value, received_value)
    
    output = report.is_informal()
    assert_instance(output, bool)
    assert_eq(output, False)
