from vampytest import returning


@returning(True)
async def test_async():
    return True


async def test_async_exception():
    raise AssertionError()
