from .. import assert_raises

from vampytest import revert, raising


def test_assert_raises():
    """
    Tests whether `raises` context-assertion succeeds.
    """
    with assert_raises(KeyError):
        raise KeyError


@revert()
def test_assert_raises_reverted():
    """
    Tests whether `raises` context-assertion fails.
    """
    with assert_raises(KeyError):
        raise ValueError


def test_assert_raises_with_subtype():
    """
    Tests whether `raises` context-assertion succeeds on subtype.
    """
    with assert_raises(LookupError):
        raise KeyError


@revert()
def test_assert_raises_with_subtype_reverted():
    """
    Tests whether `raises` context-assertion fails on 3rd type.
    """
    with assert_raises(LookupError):
        raise ValueError


def test_assert_raises_without_subtype():
    """
    Tests whether `raises` context-assertion succeeds on the type without allowing subtypes.
    """
    with assert_raises(LookupError, accept_subtypes=False):
        raise LookupError


@revert()
def test_assert_raises_without_subtype_reverted():
    """
    Tests whether `raises` context-assertion fails on subtype without allowing subtypes.
    """
    with assert_raises(LookupError, accept_subtypes=False):
        raise KeyError


@raising(ValueError)
def test_assert_raises_without_parameter():
    """
    Tests whether `raises` context-assertion raises when no parameter is given.
    """
    with assert_raises():
        pass
