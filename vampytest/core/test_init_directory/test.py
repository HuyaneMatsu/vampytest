from .. import skip

from . import pi


def test_sub_file():
    return


@skip()
def test_skipped():
    """
    I am skipped.
    """

def test_fails():
    """
    I am failing.
    """
    owo
