import vampytest


def test_print():
    capture = vampytest.capture_output()
    with capture:
        print('apple')
    
    vampytest.assert_eq(capture.get_value(), 'apple\n')
