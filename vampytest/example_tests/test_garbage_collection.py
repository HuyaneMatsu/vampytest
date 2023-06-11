import vampytest


@vampytest.with_gc(after = True, before = True)
def test_addition():
    vampytest.assert_eq(2 + 2, 4)
