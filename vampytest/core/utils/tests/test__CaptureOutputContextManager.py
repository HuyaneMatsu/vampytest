from io import StringIO

from vampytest import assert_eq, assert_instance, assert_raises

from ..capture_output_context_manager import CaptureOutputContextManager


def test__CaptureOutputContextManager__new():
    """
    Tests whether ``CaptureOutputContextManager.__new__`` works as intended.
    """
    capture = CaptureOutputContextManager()
    assert_instance(capture, CaptureOutputContextManager)
    assert_instance(capture._stream, StringIO)
    assert_instance(capture._standard_error_stream, object)
    assert_instance(capture._standard_output_stream, object)


def test_CaptureOutputContextManager__get_value():
    """
    Tests whether ``CaptureOutputContextManager.get_value`` works as intended.
    """
    value = 'Remilia'
    
    capture = CaptureOutputContextManager()
    
    with capture:
        print(value)
        print(value)
    
    output = capture.get_value()
    assert_instance(output, str)
    assert_eq(output, f'{value}\n{value}\n')


def test__CaptureOutputContextManager__nesting_same():
    """
    Tests whether ``CaptureOutputContextManager`` nesting same raises exception.
    """
    capture = CaptureOutputContextManager()
    
    with capture:
        with assert_raises(RuntimeError):
            with capture:
                pass


def test__CaptureOutputContextManager__nesting_difference():
    """
    Tests whether ``CaptureOutputContextManager`` handles nesting different correctly.
    """
    value_0 = 'Remilia'
    value_1 = 'Remilia Mama'
    
    capture_0 = CaptureOutputContextManager()
    capture_1 = CaptureOutputContextManager()
    
    with capture_0:
        print(value_0)
        with capture_1:
            print(value_1)
    
    output_0 = capture_0.get_value()
    assert_eq(output_0, f'{value_0}\n')
    
    output_1 = capture_1.get_value()
    assert_eq(output_1, f'{value_1}\n')


def test__CaptureOutputContextManager__continuous_retrieving():
    """
    Tests whether ``CaptureOutputContextManager``'s continuous retrieving works as intended.
    """
    value_0 = 'Remilia'
    value_1 = 'Remilia Mama'
    
    capture = CaptureOutputContextManager()
    
    with capture:
        print(value_0)
        output = capture.get_value()
        assert_eq(output, f'{value_0}\n')
        
        print(value_1)
        output = capture.get_value()
        assert_eq(output, f'{value_1}\n')


def test__CaptureOutputContextManager__continuous_entering():
    """
    Tests whether ``CaptureOutputContextManager`` continuous entering works.
    """
    value_0 = 'Remilia'
    value_1 = 'Remilia Mama'
    
    capture = CaptureOutputContextManager()
    
    with capture:
        print(value_0)
    
    with capture:
        print(value_1)
        
    output = capture.get_value()
    assert_eq(output, f'{value_0}\n{value_1}\n')


def test__CaptureOutputContextManager__closing():
    """
    Tests whether ``CaptureOutputContextManager`` continuous entering works.
    """
    value_0 = 'Remilia'
    value_1 = 'Remilia Mama'
    value_2 = 'Satori'
    
    capture_0 = CaptureOutputContextManager()
    capture_1 = CaptureOutputContextManager()
    
    with capture_0:
        print(value_0)
        
        with capture_1:
            pass
        
        print(value_1)
        
        with capture_1:
            pass
        
        print(value_2)
        
    output = capture_0.get_value()
    assert_eq(output, f'{value_0}\n{value_1}\n{value_2}\n')
