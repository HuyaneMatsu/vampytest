from vampytest import returning


@returning(True)
async def test_async():
    return True
