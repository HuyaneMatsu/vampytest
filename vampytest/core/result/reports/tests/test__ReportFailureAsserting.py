from ....assertions import assert_eq, assert_in, assert_instance, AssertionException, AssertionInstance

from ..failure_asserting import ReportFailureAsserting


def _assert_fields_set(report):
    """
    Asserts whether the report has all of its attributes set.
    
    Parameters
    ----------
    report : ``ReportFailureAsserting``
        The report to check.
    """
    assert_instance(report, ReportFailureAsserting)
    assert_instance(report.assertion_exception, AssertionException)


def _create_assert_exception():
    """
    Creates a new assertion exception.
    
    Returns
    -------
    assertion_exception : ``AssertionException``
    """
    assertion = AssertionInstance.__new__(AssertionInstance, 23, str)
    return AssertionException(assertion)


def test__ReportFailureAsserting__new():
    """
    Tests whether ``ReportFailureAsserting.__new__`` works as intended.
    """
    assertion_exception = _create_assert_exception()
    
    report = ReportFailureAsserting(assertion_exception)
    _assert_fields_set(report)
    
    assert_eq(report.assertion_exception, assertion_exception)


def test__ReportFailureAsserting__repr():
    """
    Tests whether ``ReportFailureAsserting.__repr__`` works as intended.
    """
    assertion_exception = _create_assert_exception()
    
    report = ReportFailureAsserting(assertion_exception)
    
    output = repr(report)
    
    assert_instance(output, str)
    assert_in(type(report).__name__, output)
    assert_in(f'assertion_exception = {assertion_exception!r}', output)


def test__ReportFailureAsserting__is_failure():
    """
    Tests whether ``ReportFailureAsserting.is_failure`` works as intended.
    """
    assertion_exception = _create_assert_exception()
    
    report = ReportFailureAsserting(assertion_exception)
    
    output = report.is_failure()
    assert_instance(output, bool)
    assert_eq(output, True)


def test__ReportFailureAsserting__is_informal():
    """
    Tests whether ``ReportFailureAsserting.is_informal`` works as intended.
    """
    assertion_exception = _create_assert_exception()
    
    report = ReportFailureAsserting(assertion_exception)
    
    output = report.is_informal()
    assert_instance(output, bool)
    assert_eq(output, False)
