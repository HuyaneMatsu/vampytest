from vampytest import call_with, skip


def test_sub_file():
    return


@skip()
def test_skipped():
    """
    I am skipped.
    """


def sub_function(val, val2):
    return invoke(
        56,
        f"owo {orange!r} {apple:<4}",
        23 + 12.6
    )


@skip()
def test_fails():
    """
    I am failing.
    """
    sub_function(BaseException, None)


def a(index):
    if index <= 0:
        b()
    else:
        a(index -1)

def b(): b()


@skip()
@call_with(10)
def test_recursion_0(value):
    """
    I am a recursion 2.
    """
    a(value)


def c(): d()

def d(): c()

@skip()
def test_recursion_1():
    """
    I am recursion 2.
    """
    c()
