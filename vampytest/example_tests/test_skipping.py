import vampytest


class MyType:
    def a():
        return 1


@vampytest.skip()
def test_repr():
    instance = MyType()
    vampytest.assert_instance(repr(instance), str)


@vampytest.skip_if(not hasattr(MyType, 'b'))
def test_repr():
    instance = MyType()
    vampytest.assert_eq(instance.b(), 2)
