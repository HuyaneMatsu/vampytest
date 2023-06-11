import vampytest


@vampytest.reverse()
def test_addition():
    vampytest.assert_eq(9 + 10, 21)
