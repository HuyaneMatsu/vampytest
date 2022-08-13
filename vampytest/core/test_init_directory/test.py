from .. import skip

from . import pi


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

def test_fails():
    """
    I am failing.
    """
    sub_function(BaseException, None)


def test_recursion():
    """
    I am a recursion.
    """
    test_recursion()


def a(index):
    if index <= 0:
        b()
    else:
        a(index -1)

def b(): b()


def test_recursion_0():
    """
    I am a recursion 2.
    """
    a(10)


def c(): d()

def d(): c()

def test_recursion_1():
    """
    I am recursion 2.
    """
    c()
