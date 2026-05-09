from vampytest import returning, raising


@returning(True)
async def test_async():
    """
    Tests whether async tests are supported.
    """
    return True


@raising(AssertionError)
async def test_async_exception():
    """
    Tests whether async exceptions are captured correctly.
    """
    raise AssertionError()
