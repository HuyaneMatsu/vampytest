from vampytest import returning


@returning(True)
async def test_async():
    """
    Tests whether async tests are supported.
    """
    return True


async def test_async_exception():
    raise AssertionError()
