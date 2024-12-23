from ....assertions import assert_eq, assert_in, assert_instance

from ..output import ReportOutput


def _assert_fields_set(report):
    """
    Asserts whether the report has all of its attributes set.
    
    Parameters
    ----------
    report : ``ReportOutput``
        The report to check.
    """
    assert_instance(report, ReportOutput)
    assert_instance(report.output, str)


def test__ReportOutput__new():
    """
    Tests whether ``ReportOutput.__new__`` works as intended.
    """
    output_value = "just testing"
    
    report = ReportOutput(output_value)
    _assert_fields_set(report)
    
    assert_eq(report.output, output_value)


def test__ReportOutput__repr():
    """
    Tests whether ``ReportOutput.__repr__`` works as intended.
    """
    output_value = "just testing"
    
    report = ReportOutput(output_value)
    
    output = repr(report)
    
    assert_instance(output, str)
    assert_in(type(report).__name__, output)
    assert_in(f'output = {output_value!r}', output)


def test__ReportOutput__is_failure():
    """
    Tests whether ``ReportOutput.is_failure`` works as intended.
    """
    output_value = "just testing"
    
    report = ReportOutput(output_value)
    
    output = report.is_failure()
    assert_instance(output, bool)
    assert_eq(output, False)


def test__ReportOutput__is_informal():
    """
    Tests whether ``ReportOutput.is_informal`` works as intended.
    """
    output_value = "just testing"
    
    report = ReportOutput(output_value)
    
    output = report.is_informal()
    assert_instance(output, bool)
    assert_eq(output, True)
