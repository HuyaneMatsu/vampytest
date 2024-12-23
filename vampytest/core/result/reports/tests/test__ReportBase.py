from ....assertions import assert_eq, assert_in, assert_instance

from ..base import ReportBase


def _assert_fields_set(report):
    """
    Asserts whether the report has all of its attributes set.
    
    Parameters
    ----------
    report : ``ReportBase``
        The report to check.
    """
    assert_instance(report, ReportBase)


def test__ReportBase__new():
    """
    Tests whether ``ReportBase.__new__`` works as intended.
    """
    report = ReportBase()
    _assert_fields_set(report)


def test__ReportBase__repr():
    """
    Tests whether ``ReportBase.__repr__`` works as intended.
    """
    report = ReportBase()
    
    output = repr(report)
    
    assert_instance(output, str)
    assert_in(type(report).__name__, output)


def test__ReportBase__is_failure():
    """
    Tests whether ``ReportBase.is_failure`` works as intended.
    """
    report = ReportBase()
    
    output = report.is_failure()
    assert_instance(output, bool)
    assert_eq(output, False)


def test__ReportBase__is_informal():
    """
    Tests whether ``ReportBase.is_informal`` works as intended.
    """
    report = ReportBase()
    
    output = report.is_informal()
    assert_instance(output, bool)
    assert_eq(output, False)
