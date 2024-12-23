from scarletio import CallableAnalyzer

from ....assertions import assert_eq, assert_in, assert_instance
from ....handling import ParameterMismatch

from ..failure_parameter_mismatch import ReportFailureParameterMismatch


def _assert_fields_set(report):
    """
    Asserts whether the report has all of its attributes set.
    
    Parameters
    ----------
    report : ``ReportFailureParameterMismatch``
        The report to check.
    """
    assert_instance(report, ReportFailureParameterMismatch)
    assert_instance(report.parameter_mismatch, ParameterMismatch)


def _create_parameter_mismatch():
    """
    Creates a new assertion exception.
    
    Returns
    -------
    parameter_mismatch : ``ParameterMismatch``
    """
    def test_function(p0, p1 = None, *p2, p3, p4 = 2, **p5):
        pass
    
    parameter_0, parameter_1, parameter_2, parameter_3, parameter_4, parameter_5 = (
        CallableAnalyzer(test_function).parameters
    )
    
    return ParameterMismatch(
        [parameter_0, parameter_1, parameter_2, parameter_3, parameter_4, parameter_5],
        None,
        None,
        [parameter_0, parameter_3],
        None,
        None,
    )


def test__ReportFailureParameterMismatch__new():
    """
    Tests whether ``ReportFailureParameterMismatch.__new__`` works as intended.
    """
    parameter_mismatch = _create_parameter_mismatch()
    
    report = ReportFailureParameterMismatch(parameter_mismatch)
    _assert_fields_set(report)
    
    assert_eq(report.parameter_mismatch, parameter_mismatch)


def test__ReportFailureParameterMismatch__repr():
    """
    Tests whether ``ReportFailureParameterMismatch.__repr__`` works as intended.
    """
    parameter_mismatch = _create_parameter_mismatch()
    
    report = ReportFailureParameterMismatch(parameter_mismatch)
    
    output = repr(report)
    
    assert_instance(output, str)
    assert_in(type(report).__name__, output)
    assert_in(f'parameter_mismatch = {parameter_mismatch!r}', output)


def test__ReportFailureParameterMismatch__is_failure():
    """
    Tests whether ``ReportFailureParameterMismatch.is_failure`` works as intended.
    """
    parameter_mismatch = _create_parameter_mismatch()
    
    report = ReportFailureParameterMismatch(parameter_mismatch)
    
    output = report.is_failure()
    assert_instance(output, bool)
    assert_eq(output, True)


def test__ReportFailureParameterMismatch__is_informal():
    """
    Tests whether ``ReportFailureParameterMismatch.is_informal`` works as intended.
    """
    parameter_mismatch = _create_parameter_mismatch()
    
    report = ReportFailureParameterMismatch(parameter_mismatch)
    
    output = report.is_informal()
    assert_instance(output, bool)
    assert_eq(output, False)
